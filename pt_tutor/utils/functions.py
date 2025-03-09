# import llm
import re
import os
import unicodedata
import pandas as pd


def clean_message(message):
    lowercased = message.lower()
    normalized = unicodedata.normalize('NFKC', lowercased)
    cleaned = re.sub(r'[^a-zA-Z0-9\s\u00C0-\u017F]', '', normalized)

    return cleaned


def get_topic_vocab(topic):
    if topic == 'Dining out':
        df = pd.read_csv('pt_tutor/vocab/dining_out.csv')
    elif topic == 'Weekend recap':
        df = pd.read_csv('pt_tutor/vocab/weekend_recap.csv')
    elif topic == 'Weather':
        df = pd.read_csv('pt_tutor/vocab/weather.csv')
    
    return df['portuguese'].str.strip().tolist()


def update_topic_vocab(sheet_url, topic_name):
    """
    Download Google Sheet as CSV using the export URL
    """
    export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    
    df = pd.read_csv(export_url)
    output_file = f'{topic_name}.csv'

    df.to_csv(output_file, index=False)
    print(f'Data saved to {output_file}')


# def update_conversation(n_submit, user_input, conversation_store):
#     if n_submit > 0 and user_input:
#         conversation_store.append({'role': 'user', 'text': user_input})
        
#         conversation_history = "\n".join([f"{entry['role'].capitalize()}: {entry['text']}" for entry in conversation_store])
        
#         response = llm.invoke(conversation_history)
#         conversation_store.append({'role': 'llm', 'text': response})
        
#         return format_conversation(conversation_store), '', conversation_store  
#     return format_conversation(conversation_store), '', conversation_store  

# # make this a seperate file eventually
# def format_conversation(conversation_store):
#     formatted_conversation = []
#     for entry in conversation_store:
#         if entry['role'] == 'user':
#             formatted_conversation.append(html.Div(f"{entry['text']}", className='user-text'))
#         else:
#             formatted_conversation.append(html.Div(f"{entry['text']}", className='llm-text'))
#     return formatted_conversation