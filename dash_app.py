import llm
import os
import math
import openai 
from langchain_openai import OpenAI
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv
import dash_dangerously_set_inner_html


app = Dash(__name__)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

llm = OpenAI(api_key=openai_api_key, organization=openai_org_id)

app.layout = html.Div([
    html.H1("Fala Português!", style={'textAlign': 'center'}),  
    html.Div(id='conversation', style={'whiteSpace': 'pre-line', 'marginBottom': '20px'}),
    html.Div([
        dcc.Input(id='user-input', type='text', placeholder='Fala aqui...', style={'width': '80%'}, n_submit=0),
    ], style={'textAlign': 'right'}),
    dcc.Store(id='conversation-store', data=[]),
], style={'width': '50%', 'margin': '0 auto'}) 

@app.callback(
    [Output('conversation', 'children'),
     Output('user-input', 'value'),  
     Output('conversation-store', 'data')],
    [Input('user-input', 'n_submit')],
    [State('user-input', 'value'), State('conversation-store', 'data')]
)
def update_conversation(n_submit, user_input, conversation_store):
    if n_submit > 0 and user_input:
        conversation_store.append({'role': 'user', 'text': user_input})
        
        conversation_history = "\n".join([f"{entry['role'].capitalize()}: {entry['text']}" for entry in conversation_store])
        
        response = llm.invoke(conversation_history)
        conversation_store.append({'role': 'llm', 'text': response})
        
        return format_conversation(conversation_store), '', conversation_store  
    return format_conversation(conversation_store), '', conversation_store  

# make this a seperate file eventually
def format_conversation(conversation_store):
    formatted_conversation = []
    for entry in conversation_store:
        if entry['role'] == 'user':
            formatted_conversation.append(html.Div(f"{entry['text']}", className='user-text'))
        else:
            formatted_conversation.append(html.Div(f"{entry['text']}", className='llm-text'))
    return formatted_conversation

# make this a seperate file eventually
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Fala Português</title>
        <style>
            .user-text {
                color: red;
                text-align: right;
            }
            .llm-text {
                color: green;
                text-align: left;
            }
            body {
                font-family: Arial, sans-serif;
            }
        </style>
    </head>
    <body>
        <div id="react-entry-point">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)