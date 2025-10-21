import os
import streamlit as st 
from wordcloud import WordCloud
from utils.graph import graph 
from utils.database import VocabDB
from utils.functions import (
    collect_custom_topic_vocab,
    get_topic_vocab,
    reset_container_content,
    translate_last,
    reset_translate_button,
    click_button,
    reset_button,
)
from utils.audio_modules import (
    record_audio,
    transcribe_audio,
    generate_audio,
)


def run_audio_chat():
    db = VocabDB()

    with st.sidebar:
        preset_topic_options = ["Comer fora 🍽️", "Resumo do fim de semana 🍺", "Tempo ⛅", "Outra tema ⁉️"]
        user_generated_topic_options = [
            topic for topic in db.load_topics(st.session_state.username)
            if topic not in preset_topic_options
        ]
        all_topic_options = preset_topic_options + user_generated_topic_options

        topic = st.sidebar.radio(
            "**Escolhe o tema que queres discutir e diz as palavras abaixo:**",
            key="topic",
            options=all_topic_options,
        )
        if topic == "Outra tema ⁉️":
            topic_submission = st.text_input("Escreve o teu tema aqui:", key="custom_topic", value="opening a new bank account")
        else:   
            topic_submission = topic

        if topic_submission != st.session_state.topic_submission: #initializing 
            st.session_state.correct_count = db.load_progress(st.session_state.username, topic_submission)[0]
            st.session_state.last_correct_word = db.load_progress(st.session_state.username, topic_submission)[1]

            if not st.session_state.correct_count: # no progress saved for username and topic.
                if topic_submission in ["Comer fora 🍽️", "Resumo do fim de semana 🍺", "Tempo ⛅"]:
                    st.session_state.correct_count = get_topic_vocab(topic_submission)
                else:
                    st.session_state.correct_count = collect_custom_topic_vocab(topic_submission)

            st.session_state.topic_submission = topic_submission
            reset_container_content()

        mastered_words = {word: count for word, count in st.session_state.correct_count.items() if count > 0}
        remaining_words = {word: 1 for word, count in st.session_state.correct_count.items() if count == 0} # set to 1 for wordcloud

        if len(remaining_words) > 0:
            remaining_word_wordcloud = WordCloud(
                width=800, 
                height=425,
                background_color='white',
                min_font_size=20,
                max_font_size=20,
                random_state=42).generate_from_frequencies(remaining_words)
            st.sidebar.image(remaining_word_wordcloud.to_image(), use_container_width=True)

        st.sidebar.write("**Palavras corretas**")

        col1, col2 = st.sidebar.columns(2)
        col1.markdown(f"<div class='box-style'>Última: <strong style='font-size:1.4em'>{st.session_state.last_correct_word}</strong></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='box-style'>Totais: <strong style='font-size:1.4em'>{len(mastered_words)}</strong></div>", unsafe_allow_html=True)
    
        if len(mastered_words) > 0:
            correct_word_wordcloud = WordCloud(
                width=800, 
                height=425,
                background_color='white',
                min_font_size=5,
                max_font_size=100,
                random_state=42).generate_from_frequencies(mastered_words) # mastered_words replaces st.session_state.correct_count
            st.sidebar.image(correct_word_wordcloud.to_image(), use_container_width=True)

        st.sidebar.button(label="GUARDAR", key='launch', type="primary", on_click=click_button)
        if st.session_state.clicked:
            db.save_progress(st.session_state.username, topic_submission, st.session_state.correct_count, st.session_state.last_correct_word)
            st.sidebar.write("Guardado!")
            reset_button()

    st.write("## Fala Português!")

    # starting main section 
    main_container = st.container()

    with main_container:
        messages_container = st.container()
        chat_area = messages_container.container(height=400)

        for i in range(len(st.session_state.student_messages)):
            with chat_area.chat_message(name="student", avatar="😊"):
                st.markdown(f"<div class='student-style'>{st.session_state.student_messages[i]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='student-correction-style'>{st.session_state.student_correction_messages[i]}</div>", unsafe_allow_html=True)
            with chat_area.chat_message(name="tutor", avatar="🤖"):
                st.markdown(f"<div class='tutor-style'>{st.session_state.tutor_messages[i]}</div>", unsafe_allow_html=True)
                if i == len(st.session_state.student_messages) - 1:
                    if st.session_state.clicked_translate:
                        st.markdown(f"""<div class='tutor-translate-style'>{st.session_state.last_tutor_message_translated}</div>""", unsafe_allow_html=True)
                        reset_translate_button()
                    else:
                        st.button(label="Traduzir última", key='translate', type="secondary", on_click=translate_last)

                    response_file = 'pt_tutor/data/audio/response.mp3'
                    generate_audio(st.session_state.tutor_messages[-1], response_file)
                    st.audio(data=response_file, autoplay=True)

    if recording := st.audio_input(label="Fala aqui..."):
        question_file = 'pt_tutor/data/audio/question.wav'
        record_audio(recording, question_file)
        transcription = transcribe_audio(question_file)

        with chat_area.chat_message(name="student", avatar="😊"):
            st.markdown(f"<div class='student-style'>{transcription}</div>", unsafe_allow_html=True)
            st.session_state.student_messages.append(transcription)

            response = graph.invoke(
                {
                    "messages": [transcription], 
                    "core_convo": [transcription],
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
            st.session_state.correct_count = response["correct_count"]
            st.session_state.last_correct_word = response["last_correct_word"]

            tutor_response = response["core_convo"][-1].content
            st.session_state.tutor_messages.append(tutor_response)
        
            st.rerun()
