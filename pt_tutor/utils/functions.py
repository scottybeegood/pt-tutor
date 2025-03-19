import streamlit as st 
import re
import os
import unicodedata
import pandas as pd


def clean_message(message):
    lowercased = message.lower()
    normalized = unicodedata.normalize('NFKC', lowercased)
    cleaned = re.sub(r'[^a-zA-Z0-9\s\u00C0-\u017F]', '', normalized)

    return cleaned


def get_filpath(topic):
    if topic == 'Comer fora 🍽️':
        filepath = 'pt_tutor/vocab/dining_out.csv'
    elif topic == 'Resumo do fim de semana 🍺':
        filepath = 'pt_tutor/vocab/weekend_recap.csv'
    elif topic == 'Tempo ⛅':
        filepath = 'pt_tutor/vocab/weather.csv'

    return filepath 


def get_topic_vocab(topic):
    filepath = get_filpath(topic)
    df = pd.read_csv(filepath)
    topic_vocab = set(df['portuguese'].str.strip())

    return topic_vocab


def load_progress(topic):
    filepath = get_filpath(topic)
    df = pd.read_csv(filepath)

    correct_count = df.set_index('portuguese')['correct_count'].to_dict()
    correct_count = {k: v for k, v in correct_count.items() if v > 0}

    try:
        last_correct_word = df.loc[df['flag_last_correct_word'] == 1, 'portuguese'].iloc[0]
    except IndexError:
        last_correct_word = ''
    
    return (correct_count, last_correct_word)


def click_button():
    st.session_state.clicked = True


def reset_button():
    st.session_state.clicked = False


def save_progress(topic, correct_count, last_correct_word):
    filepath = get_filpath(topic)
    df = pd.read_csv(filepath)
    df['correct_count'] = df['portuguese'].map(correct_count)

    df['flag_last_correct_word'] = 0 # reset before saving
    df.loc[df['portuguese']==last_correct_word, 'flag_last_correct_word'] = 1

    df.to_csv(filepath, index=False)


def update_topic_vocab(sheet_url, topic_name):
    export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    
    df = pd.read_csv(export_url)
    output_file = f'{topic_name}.csv'

    df.to_csv(output_file, index=False)
    print(f'Data saved to {output_file}')
