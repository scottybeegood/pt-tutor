import streamlit as st 
import re
import unicodedata
import pandas as pd
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from utils.instructions import (
    custom_topic_vocab_collector_instructions, 
    translator_instructions
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID") or st.secrets.get("OPENAI_ORG_ID")

llm = ChatOpenAI(
    api_key=openai_api_key,
    organization=openai_org_id,
    model="gpt-4-turbo",
    temperature=1.0
)


def submit_username():
    st.session_state.username = st.session_state.temp_username
    st.session_state.username_submitted = True
    st.session_state.temp_username = ""


def set_chat_mode():
    if st.session_state.temp_chat_mode == "Áudio 🎤👨":
        st.session_state.chat_mode = "audio" 
        st.session_state.voice_model = "Sadaltager"
    if st.session_state.temp_chat_mode == "Áudio 🎤👩":
        st.session_state.chat_mode = "audio" 
        st.session_state.voice_model = "Achernar"
    if st.session_state.temp_chat_mode == "Texto 💬":
        st.session_state.chat_mode = "text"
        
    st.session_state.chat_mode_submitted = True
    st.session_state.temp_chat_mode = ""


def collect_custom_topic_vocab(topic):
    system_message = custom_topic_vocab_collector_instructions.format(topic=topic)
    response = llm.invoke([SystemMessage(content=system_message)])
    topic_vocab_dict = {word.strip(): 0 for word in response.content.split(",") if word.strip()}

    return topic_vocab_dict
    

def clean_message(message):
    lowercased = message.lower()
    normalized = unicodedata.normalize('NFKC', lowercased)
    cleaned = re.sub(r'[^a-zA-Z0-9\s\u00C0-\u017F]', '', normalized)

    return cleaned


def reset_container_content():
    st.session_state.student_messages = []
    st.session_state.tutor_messages = []
    st.session_state.clicked_translate = False
    st.session_state.last_tutor_message_translated = ""
    st.session_state.student_correction_messages = []


def get_filepath(topic):
    if topic == 'Comer fora 🍽️': 
        filepath = 'pt_tutor/data/seed_vocab/dining_out.csv'
    elif topic == 'Resumo do fim de semana 🍺':
        filepath = 'pt_tutor/data/seed_vocab/weekend_recap.csv'
    elif topic == 'Tempo ⛅':
        filepath = 'pt_tutor/data/seed_vocab/weather.csv'
    return filepath 


def get_topic_vocab(topic):
    filepath = get_filepath(topic)
    df = pd.read_csv(filepath)
    topic_vocab_dict = {word.strip(): 0 for word in df['portuguese'].str.strip()}

    return topic_vocab_dict


def translate_last():
    st.session_state.clicked_translate = True

    last_tutor_message = st.session_state.tutor_messages[-1]

    system_message = translator_instructions.format(message=last_tutor_message)
    response = llm.invoke([SystemMessage(content=system_message)])

    st.session_state.last_tutor_message_translated = response.content


def reset_translate_button():
    st.session_state.clicked_translate = False

    st.session_state.last_tutor_message_translated = ""


def click_save_button():
    st.session_state.save_clicked = True


def reset_save_button():
    st.session_state.save_clicked = False


def click_speak_button():
    st.session_state.speak_clicked = True


def reset_speak_button():
    st.session_state.speak_clicked = False
