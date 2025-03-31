import sqlite3
import pandas as pd


class VocabDB:
    def __init__(self):
        self.db_path = 'pt_tutor/data/.streamlit/portuguese_app.db'
        self.topic_filepath = {
            'Comer fora 🍽️': 'pt_tutor/data/seed_vocab/dining_out.csv', 
            'Resumo do fim de semana 🍺': 'pt_tutor/data/seed_vocab/weekend_recap.csv',
            'Tempo ⛅': 'pt_tutor/data/seed_vocab/weather.csv',
        }
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS progress (
                    username TEXT,
                    topic TEXT,
                    portuguese_word TEXT,
                    correct_count INTEGER,
                    flag_last_correct_word INTEGER
                )
            ''')
            conn.commit()


    def load_progress(self, username: str, topic: str):
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("""
                select portuguese_word, correct_count, flag_last_correct_word
                from progress
                where username = ? and topic = ?
            """, conn, params=(username, topic))

            correct_count = df.set_index('portuguese_word')['correct_count'].to_dict()
            correct_count = {k: v for k, v in correct_count.items() if v > 0}

            try:
                last_correct_word = df.loc[df['flag_last_correct_word'] == 1, 'portuguese_word'].iloc[0]
            except IndexError:
                last_correct_word = ''
        
            return (correct_count, last_correct_word)
        

    def save_progress(self, username: str, topic: str, correct_count: dict, last_correct_word: str):
        words = list(correct_count.keys())
        df = pd.DataFrame({
            'username': username,
            'topic': topic,
            'portuguese_word': words,
            'correct_count': [correct_count[word] for word in words],
            'flag_last_correct_word': [1 if word == last_correct_word else 0 for word in words]
        })

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('delete from progress where username = ? and topic = ?', (username, topic))

            df.to_sql('progress', conn, if_exists='append', index=False)
