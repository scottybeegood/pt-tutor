import streamlit as st 
import uuid
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils.graph import graph 
from utils.functions import (
    get_topic_vocab,
    get_mastered_words,
    click_button,
    reset_button,
    save_mastered_words,
)

st.set_page_config(layout="wide", page_title="Fala Português!")

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
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "student_messages" not in st.session_state:
    st.session_state.student_messages = []
if "student_correction_messages" not in st.session_state:
    st.session_state.student_correction_messages = []
if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []
if "topic_vocab" not in st.session_state:
    st.session_state.topic_vocab = set()
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "mastered_words" not in st.session_state:
    st.session_state.mastered_words = set()
if "last_mastered_word" not in st.session_state:
    st.session_state.last_mastered_word = ""

st.write("## Fala Português!")

sidebar = st.sidebar

with sidebar:
    topic = st.sidebar.radio(
        "Select the topic you'd like to discuss:",
        key="topic",
        options=["Dining out", "Weekend recap", "Weather"],
    )
    topic_vocab = get_topic_vocab(topic)
    print(f'get_topic_vocabs: {topic_vocab}')
    print(f'ss topic vocab: {st.session_state.topic_vocab}')
    if topic_vocab != st.session_state.topic_vocab:
        st.session_state.mastered_words = get_mastered_words(topic)
    # print(f'ss mastered words post: {st.session_state.mastered_words}')
    st.session_state.topic_vocab = topic_vocab

    st.sidebar.write('Remaining Unmastered Words:')
    unmastered_word_set = topic_vocab - st.session_state.mastered_words
    unmastered_word_dict = {word: 1 for word in unmastered_word_set}
    unmastered_wordcloud = WordCloud(width=800, 
                                     height=350,
                                     background_color='white',
                                     min_font_size=20,
                                     max_font_size=20,
                                     random_state=42).generate_from_frequencies(unmastered_word_dict)
    st.sidebar.image(unmastered_wordcloud.to_image(), use_container_width=True)

    st.sidebar.write(f'Last Mastered Word: {st.session_state.last_mastered_word}')

    st.sidebar.write('Mastered Words:')
    print(f'ss mastered words: {st.session_state.mastered_words}')
    if len(st.session_state.mastered_words) > 0:
        mastered_word_dict = {word: 1 for word in st.session_state.mastered_words}
        mastered_wordcloud = WordCloud(width=800, 
                                       height=350,
                                       background_color='white',
                                       min_font_size=20,
                                       max_font_size=20,
                                       random_state=42).generate_from_frequencies(mastered_word_dict)
        st.sidebar.image(mastered_wordcloud.to_image(), use_container_width=True)

    score = len(st.session_state.mastered_words) / len(topic_vocab)
    st.sidebar.write(f'Topic Score: {score}')

    st.sidebar.button("SAVE", key='launch', type="primary", on_click=click_button)
    if st.session_state.clicked:
        save_mastered_words(topic, st.session_state.mastered_words)
        st.sidebar.write("Saved!")
        reset_button()


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
                "mastered_words": st.session_state.mastered_words,
                "last_mastered_word": "",
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

        st.session_state.mastered_words = response["mastered_words"]
        if response["last_mastered_word"] != st.session_state.last_mastered_word:
            st.session_state.last_mastered_word = response["last_mastered_word"]
            st.rerun()
