import streamlit as st 
import plotly.graph_objects as go
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from utils.graph import graph 

st.set_page_config(layout="wide", page_title="Fala Português!")

st.markdown("""
    <style>  
    .tutor-style {
        color: darkgreen !important;
        font-size: 20px !important;
        text-align: left !important;
    }
    .student-style {
        color: darkred !important;
        font-size: 20px !important;
        text-align: right !important;
    }
    .student-correction-style {
        color: grey !important;
        font-style: italic !important;
        font-size: 16px !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

st.write("## Fala Português!")

sidebar = st.sidebar
sidebar_col = st.columns([1, 2])[0]

with sidebar:
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

main_container = st.container()

with main_container:
    messages_container1 = st.container()
    chat_area = messages_container1.container(height=400)

if prompt := st.chat_input("Fala aqui..."):
    with chat_area.chat_message("student", avatar=None):
        st.markdown(f"<div class='student-style'>{prompt}</div>", unsafe_allow_html=True)

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
        student_correction = response["corrections"][-1].content

        # st.markdown(f"<div class='student-style'>{prompt}</div>", unsafe_allow_html=True)
        st.markdown(f"""<div class='student-correction-style'>{student_correction}</div>""", unsafe_allow_html=True)

    with chat_area.chat_message("tutor", avatar=None):
        # st_callback = StreamlitCallbackHandler(col1.container())


        tutor_response = response["core_convo"][-1].content
        st.markdown(f"<div class='tutor-style'>{tutor_response}</div>", unsafe_allow_html=True)
        
        # feedback_area.write(response["corrections"][-1].content)


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
