import os 
from dotenv import load_dotenv
load_dotenv()
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("CWD:", os.getcwd())

import streamlit as st 
from wordcloud import WordCloud
import audio_chat
import text_chat
from utils.graph import graph 
from utils.database import VocabDB
from utils.functions import (
    submit_username,
    set_chat_mode,
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
if 'chat_mode' not in st.session_state:
    st.session_state.chat_mode = ""
if 'temp_chat_mode' not in st.session_state:
    st.session_state.temp_chat_mode = ""
if 'chat_mode_submitted' not in st.session_state:
    st.session_state.chat_mode_submitted = False
if "student_messages" not in st.session_state:
    st.session_state.student_messages = []
if "student_correction_messages" not in st.session_state:
    st.session_state.student_correction_messages = []
if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []
if "last_tutor_message_translated" not in st.session_state:
    st.session_state.last_tutor_message_translated = ""
if "topic_vocab" not in st.session_state:
    st.session_state.topic_vocab = set() # needed to recognize topic changes 
if "correct_count" not in st.session_state:
    st.session_state.correct_count = {}
if "last_correct_word" not in st.session_state:
    st.session_state.last_correct_word = ""
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "audio_running" not in st.session_state:
    st.session_state.audio_running = False


if not st.session_state.username_submitted:
    st.sidebar.text_input(
        "**Crie ou insira o seu nome de perfil:**",
        key="temp_username",
        on_change=submit_username,
    )
else:
    st.sidebar.write(f"Olá, {st.session_state.username}!")

    if not st.session_state.chat_mode_submitted:
        st.sidebar.radio(
            "**Escolhe o modo de chat:**",
            key="temp_chat_mode",
            options=["Texto 💬", "Áudio 🎤"],
            index=None,
            on_change=set_chat_mode,
        )
    else:
        if st.session_state.chat_mode == "text":
            text_chat.run_text_chat()
        else: 
            audio_chat.run_audio_chat()
    