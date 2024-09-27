from dash import Input, Output, html, dcc, callback, Dash
import llm

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = Dash(__name__)

docs = ['transcript1.txt', 'transcript2.txt']
app.layout = html.Div([
    doc := dcc.Dropdown(docs, 'transcript1.txt'),
    html.Label(f'Ask a question: '),
    question := dcc.Textarea(),
    output := html.Div()
])

@callback(
        Output(output, 'children'), 
        Input(question, 'value'), 
        Input(doc, 'value')
)

def update(question, selected_doc):
    if not selected_doc in docs:
         return 'Document not found'

    with open(selected_doc, 'r') as f:
        content = f.read()
    
    model = llm.get_model("llama2")

    prompt = (
        'Answer the following question based off of the following document:\n' +
        'question: ' + question + '\n'
        'document:\n' + content
    )

    response = model.prompt(prompt_value).text()

    return response 

if __name__ == '__main__':
    app.run_server(debug=True)  
    