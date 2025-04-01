import streamlit as st 
from wordcloud import WordCloud
from utils.graph import graph 
from utils.database import VocabDB
from utils.functions import (
    submit_username,
    get_topic_vocab,
    click_button,
    reset_button,
    
)

st.set_page_config(layout="wide")

st.markdown("""
    <style>  
    .tutor-style {
        color: darkgreen !important;
        font-size: 20px !important;
        text-align: left !important;
    }
    .student-style {
        color: darkred !important;
        font-size: 20px !important;
        text-align: right !important;
    }
    .student-correction-style {
        color: grey !important;
        font-style: italic !important;
        font-size: 16px !important;
        text-align: right !important;
    }
    .box-style {
        border: 2px solid green !important;
        padding: 10px !important;
        border-radius: 5px !important;
        text-align: center !important;
        margin-bottom: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

if "username" not in st.session_state:
    st.session_state.username = ""
if "temp_username" not in st.session_state:
    st.session_state.temp_username = ""
if 'username_submitted' not in st.session_state:
    st.session_state.username_submitted = False
if "student_messages" not in st.session_state:
    st.session_state.student_messages = []
if "student_correction_messages" not in st.session_state:
    st.session_state.student_correction_messages = []
if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []
if "topic_vocab" not in st.session_state:
    st.session_state.topic_vocab = set() # needed to recognize topic changes 
if "correct_count" not in st.session_state:
    st.session_state.correct_count = {}
if "last_correct_word" not in st.session_state:
    st.session_state.last_correct_word = ""
if "clicked" not in st.session_state:
    st.session_state.clicked = False

db = VocabDB()

sidebar = st.sidebar

if not st.session_state.username_submitted:
    st.sidebar.text_input(
        "**Crie ou insira o seu nome de perfil:**",
        key="temp_username",
        on_change=submit_username,
    )
else:
    st.sidebar.write(f"Olá, {st.session_state.username}!")

    with sidebar:
        topic = st.sidebar.radio(
            "**Escolhe o tema que queres discutir e diz as palavras abaixo:**",
            key="topic",
            options=["Comer fora 🍽️", "Resumo do fim de semana 🍺", "Tempo ⛅"],
        )
        topic_vocab = get_topic_vocab(topic)
        if topic_vocab != st.session_state.topic_vocab:
            st.session_state.correct_count = db.load_progress(st.session_state.username, topic)[0]
            st.session_state.last_correct_word = db.load_progress(st.session_state.username, topic)[1]

        st.session_state.topic_vocab = topic_vocab

        remaining_words = topic_vocab - set(st.session_state.correct_count)
        remaining_word_dict = {word: 1 for word in remaining_words}
        remaining_word_wordcloud = WordCloud(
            width=800, 
            height=425,
            background_color='white',
            min_font_size=20,
            max_font_size=20,
            random_state=42).generate_from_frequencies(remaining_word_dict)
        st.sidebar.image(remaining_word_wordcloud.to_image(), use_container_width=True)

        st.sidebar.write("**Palavras corretas**")

        col1, col2 = st.sidebar.columns(2)
        col1.markdown(f"<div class='box-style'>Última: <strong style='font-size:1.4em'>{st.session_state.last_correct_word}</strong></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='box-style'>Totais: <strong style='font-size:1.4em'>{len(st.session_state.correct_count)}</strong></div>", unsafe_allow_html=True)
    
        if len(st.session_state.correct_count) > 0:
            correct_word_wordcloud = WordCloud(
                width=800, 
                height=425,
                background_color='white',
                min_font_size=5,
                max_font_size=100,
                random_state=42).generate_from_frequencies(st.session_state.correct_count)
            st.sidebar.image(correct_word_wordcloud.to_image(), use_container_width=True)

        st.sidebar.button("GUARDAR", key='launch', type="primary", on_click=click_button)
        if st.session_state.clicked:
            db.save_progress(st.session_state.username, topic, st.session_state.correct_count, st.session_state.last_correct_word)
            st.sidebar.write("Guardado!")
            reset_button()

    st.write("## Fala Português!")

    main_container = st.container()

    with main_container:
        messages_container = st.container()
        chat_area = messages_container.container(height=400)

        for i in range(len(st.session_state.student_messages)):
            with chat_area.chat_message("student", avatar="😊"):
                st.markdown(f"<div class='student-style'>{st.session_state.student_messages[i]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='student-correction-style'>{st.session_state.student_correction_messages[i]}</div>", unsafe_allow_html=True)
            with chat_area.chat_message("tutor", avatar="🤖"):
                st.markdown(f"<div class='tutor-style'>{st.session_state.tutor_messages[i]}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Fala aqui..."):
        with chat_area.chat_message("student", avatar="😊"):
            st.markdown(f"<div class='student-style'>{prompt}</div>", unsafe_allow_html=True)
            st.session_state.student_messages.append(prompt)

            response = graph.invoke(
                {
                    "messages": [prompt], 
                    "core_convo": [prompt],
                    "topic_vocab": topic_vocab,
                    "correct_count": st.session_state.correct_count,
                    "last_correct_word": st.session_state.last_correct_word,
                    "topic": topic
                },
                config = {
                    "configurable": {"thread_id": 42},
                }
            )
            student_correction = response["corrections"][-1].content
            st.session_state.student_correction_messages.append(student_correction)
            st.markdown(f"""<div class='student-correction-style'>{student_correction}</div>""", unsafe_allow_html=True)

        with chat_area.chat_message("tutor", avatar="🤖"):
            tutor_response = response["core_convo"][-1].content
            st.session_state.tutor_messages.append(tutor_response)
            st.markdown(f"<div class='tutor-style'>{tutor_response}</div>", unsafe_allow_html=True)

            st.session_state.correct_count = response["correct_count"]
            if response["last_correct_word"] != st.session_state.last_correct_word:
                st.session_state.last_correct_word = response["last_correct_word"]
                st.rerun()
