import streamlit as st 
import uuid
import plotly.graph_objects as go
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from utils.graph import graph 
from langchain_core.messages import (
    AIMessage, 
    BaseMessage, 
    HumanMessage, 
    SystemMessage
)

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

if "messages" not in st.session_state:
    st.session_state.messages = []
if "student_messages" not in st.session_state:
    st.session_state.student_messages = []
if "student_correction_messages" not in st.session_state:
    st.session_state.student_correction_messages = []
if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

st.write("## Fala Português!")

sidebar = st.sidebar
sidebar_col = st.columns([1, 2])[0]

with sidebar:
    user = st.sidebar.text_input(
        "Select your name or add a new one:",
        key="user",
    )

    topic = st.sidebar.radio(
        "Select the topic you'd like to discuss:",
        key="topic",
        options=["Dining out", "Weekend recap", "Weather"],
    )

main_container = st.container()

with main_container:
    messages_container = st.container()
    chat_area = messages_container.container(height=400)

    # replace logic below with a counter i from 1 that scans that the keys in st.session_state (core_convo and corrections)
    for i in range(len(st.session_state.student_messages)):
        with chat_area.chat_message("student", avatar="😊"):
            st.markdown(f"<div class='student-style'>{st.session_state.student_messages[i]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='student-correction-style'>{st.session_state.student_correction_messages[i]}</div>", unsafe_allow_html=True)
        with chat_area.chat_message("tutor", avatar="🤖"):
            st.markdown(f"<div class='tutor-style'>{st.session_state.tutor_messages[i]}</div>", unsafe_allow_html=True)


    
    # for message in st.session_state.messages:
    #     if type(message) is AIMessage:
    #         chat_area.chat_message("tutor", avatar="🤖").markdown(f"<div class='tutor-style'>{message.content}</div>", unsafe_allow_html=True)
    #     if type(message) is HumanMessage:
    #         chat_area.chat_message("student", avatar="😊").markdown(f"<div class='student-style'>{message.content}</div>", unsafe_allow_html=True)
    #     if type(message) is SystemMessage:
    #         chat_area.chat_message("corrector", avatar="✅").markdown(f"<div class='student-correction-style'>{message.content}</div>", unsafe_allow_html=True)

    # for message in st.session_state.core_convo:
    #     if type(message) is AIMessage:
    #         chat_area.chat_message("tutor", avatar="🤖").markdown(f"<div class='tutor-style'>{message.content}</div>", unsafe_allow_html=True)
    #     if type(message) is HumanMessage:
    #         chat_area.chat_message("student", avatar="😊").markdown(f"<div class='student-style'>{message.content}</div>", unsafe_allow_html=True)

    # for message in st.session_state.corrections:


if prompt := st.chat_input("Fala aqui..."):
    with chat_area.chat_message("student", avatar="😊"):
        st.markdown(f"<div class='student-style'>{prompt}</div>", unsafe_allow_html=True)
        st.session_state.student_messages.append(prompt)

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

        # st.markdown(f"<div class='student-style'>{prompt}</div>", unsafe_allow_html=True) #move up to display earlier
        st.markdown(f"""<div class='student-correction-style'>{student_correction}</div>""", unsafe_allow_html=True)
        st.session_state.student_correction_messages.append(student_correction)

    with chat_area.chat_message("tutor", avatar="🤖"):
        # st_callback = StreamlitCallbackHandler(col1.container())


        tutor_response = response["core_convo"][-1].content
        st.session_state.tutor_messages.append(tutor_response)
        st.markdown(f"<div class='tutor-style'>{tutor_response}</div>", unsafe_allow_html=True)


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
