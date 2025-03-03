import streamlit as st 
import plotly.graph_objects as go
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from utils.graph import graph 

st.set_page_config(layout="wide", page_title="Fala Português!")

st.write("## Fala Português!")

user = st.sidebar.text_input(
    "Select your name or add a new one:",
    key="user",
)
st.sidebar.write("Active user:", user)

topic = st.sidebar.radio(
    "Select the topic you'd like to discuss:",
    key="topic",
    options=["Dining out", "Weekend recap", "Weather"],
)

# st.sidebar.title("Word use frequency")

col1, col2 = st.columns(2)

col1.write("Fala aqui...")
col2.write("Feedback on responses here...")

messages_container1 = col1.container(height=500)
messages_container2 = col2.container(height=500)

if prompt := col1.chat_input():
    messages_container1.chat_message("user").write(prompt)

    with messages_container1.chat_message("assistant"):
        # st_callback = StreamlitCallbackHandler(col1.container())

        response = graph.invoke(
            {
                "messages": [prompt], 
                "core_convo": [prompt],
                "mastered_words": {}, #TODO: pipe in mastered words
                "topic": topic
            },
            config = {
                "configurable": {"thread_id": 42}, 
                # "callbacks": [st_callback]
            }
        )
        messages_container1.write(response["core_convo"][-1].content)
        # col2.write(response["corrections"][-1].content)
        messages_container2.write(response["corrections"][-1].content)


# SIDEBAR 
        words = list(response["correct_words"].keys())
        counts = list(response["correct_words"].values())

        if len(words) > 0:
            sorted_data = sorted(zip(counts, words), reverse=False)
            counts, words = zip(*sorted_data)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=words, 
            x=counts,
            orientation='h',
            marker=dict(color='blue')
        ))

        fig.update_layout(
            title="Word Frequencies",
            xaxis_title="Count",
            yaxis_title="Words",
            height=400,
            margin=dict(l=0, r=0, t=30, b=30)
        )

        st.sidebar.plotly_chart(fig, use_container_width=True)
