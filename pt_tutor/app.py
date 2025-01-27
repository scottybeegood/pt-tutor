import streamlit as st 
import plotly.graph_objects as go
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from utils.graph import graph 
# from utils.graph import(
#     #State, 
#     build_graph
# )

st.set_page_config(layout="wide", page_title="Fala Português!")

st.write("## Fala Português!")

st.sidebar.radio(
    "Select your name or add a new one:",
    key="user",
    options=["Scott", "Bianca", "New user"],
)

topic = st.sidebar.radio(
    "Select the topic you'd like to discuss:",
    key="topic",
    options=["Dining out", "Weekend recap", "Weather"],
)

# graph = build_graph(topic)

# st.sidebar.title("Word use frequency")

col1, col2 = st.columns(2)

col1.write("Fala aqui...")
col2.write("Feedback on responses here...")

if prompt := col1.chat_input():
    col1.chat_message("user").write(prompt)

    with col1.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(col1.container())

        response = graph.invoke(
            {
                "messages": [prompt], 
                "core_convo": [prompt],
                "topic": topic
            },
            config = {
                "configurable": {"thread_id": 42}, 
                "callbacks": [st_callback]
            }
        )
        col1.write(response["core_convo"][-1].content)
        col2.write(response["corrections"][-1].content)


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
