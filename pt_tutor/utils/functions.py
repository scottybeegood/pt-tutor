# import llm
import re
import unicodedata

def clean_message(message):
    lowercased = message.lower()
    normalized = unicodedata.normalize('NFKC', lowercased)
    cleaned = re.sub(r'[^a-zA-Z0-9\s\u00C0-\u017F]', '', normalized)

    return cleaned


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