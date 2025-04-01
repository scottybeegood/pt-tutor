import sqlite3
import streamlit as st
from st_supabase_connection import SupabaseConnection
import pandas as pd
import os
from dotenv import load_dotenv


class VocabDB:
    def __init__(self):
        load_dotenv()
        self.init_database()


    def init_database(self):
        conn = st.connection("supabase",type=SupabaseConnection)
        self.supabase = conn.client
   

    def load_progress(self, username: str, topic: str):
        conn = st.connection("supabase", type=SupabaseConnection)
        result = (conn.client.table('progress')
                    .select('portuguese_word, correct_count, flag_last_correct_word')
                    .eq('username', username)
                    .eq('topic', topic)
                    .execute())
        df = pd.DataFrame(result.data)

        if df.empty:
            return ({}, '')

        correct_count = df.set_index('portuguese_word')['correct_count'].to_dict()
        correct_count = {k: v for k, v in correct_count.items() if v > 0}

        try:
            last_correct_word = df.loc[df['flag_last_correct_word'] == 1, 'portuguese_word'].iloc[0]
        except IndexError:
            last_correct_word = ''
    
        return (correct_count, last_correct_word)
        

    def save_progress(self, username: str, topic: str, correct_count: dict, last_correct_word: str):
        words = list(correct_count.keys())
        progress = [
            {
                'username': username,
                'topic': topic,
                'portuguese_word': word,
                'correct_count': correct_count[word],
                'flag_last_correct_word': 1 if word == last_correct_word else 0
            }
            for word in words
        ]

        conn = st.connection("supabase", type=SupabaseConnection)
        (conn.client.table('progress')
            .delete()
            .eq('username', username)
            .eq('topic', topic)
            .execute())
        
        if progress:
            (conn.client.table('progress')
                .insert(progress)
                .execute())
