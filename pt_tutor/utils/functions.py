import streamlit as st 
import re
import os
import unicodedata
import pandas as pd


def submit_username():
    st.session_state.username = st.session_state.temp_username
    st.session_state.username_submitted = True
    st.session_state.temp_username = ""


def clean_message(message):
    lowercased = message.lower()
    normalized = unicodedata.normalize('NFKC', lowercased)
    cleaned = re.sub(r'[^a-zA-Z0-9\s\u00C0-\u017F]', '', normalized)

    return cleaned


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
    topic_vocab = set(df['portuguese'].str.strip())

    return topic_vocab


def click_button():
    st.session_state.clicked = True


def reset_button():
    st.session_state.clicked = False
