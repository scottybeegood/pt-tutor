import os
import streamlit as st
import random

from dotenv import load_dotenv
from typing import Annotated

from langchain_core.messages import (
    HumanMessage, 
    SystemMessage, 
    AIMessage
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import (
    START, 
    StateGraph, 
    END
)
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI

from utils.instructions import (
    chatbot_instructions,
    corrector_instructions
)
from utils.functions import (
    clean_message,
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID") or st.secrets.get("OPENAI_ORG_ID")

llm = ChatOpenAI(
    api_key=openai_api_key,
    organization=openai_org_id,
    model="gpt-3.5-turbo",
    temperature=1.0,
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    core_convo: Annotated[list, add_messages]
    corrections: Annotated[list, add_messages]
    correct_count: dict
    last_correct_word: str
    topic: str 

class ResponseDict(TypedDict):
    """
    A structured list of dictionaries representing the alternative chatbot responses 
    """
    responses: list[dict]


def chatbot(state: State):
    topic = state["topic"]
    correct_vocab = {word for word, count in state["correct_count"].items() if count > 0}

    system_message = chatbot_instructions.format(topic=topic, 
                                                 correct_vocab=correct_vocab)
    structured_llm = llm.with_structured_output(ResponseDict)
    response = structured_llm.invoke([SystemMessage(content=system_message)]+state["messages"])

    try: 
        response_list = response["responses"]
        selected_response = random.choice(response_list)
        selected_text = selected_response["text"]
    except:
        selected_text = "Pode repetir?"
        
    selected_text_ai_message = AIMessage(content=selected_text)

    return {
        "messages": [selected_text_ai_message],
        "core_convo": [selected_text_ai_message]
    }


def corrector(state: State):
    user_message = next(
        (m.content for m in reversed(state['core_convo']) if isinstance(m, HumanMessage)),
        None
    )

    system_message = corrector_instructions.format(user_message=user_message)
    response = llm.invoke([SystemMessage(content=system_message)]+state["messages"])

    return {
        "corrections": [response]
    }


def scorer(state: State):
    user_message = next(
        (m.content for m in reversed(state['core_convo']) if isinstance(m, HumanMessage)),
        None
    )
    user_message = clean_message(user_message)
    corrector_message = next(
        (m.content for m in reversed(state['corrections']) if isinstance(m, AIMessage)),
        None
    )
    corrector_message = clean_message(corrector_message)

    updated_correct_count = state["correct_count"].copy() # dicts are mutable
    updated_last_correct_word = state["last_correct_word"]

    for user_word in corrector_message.split():
        if user_word in user_message.split() and user_word in updated_correct_count.keys():
            updated_correct_count[user_word] += 1
            updated_last_correct_word = user_word

    return {
        "correct_count": updated_correct_count,
        "last_correct_word": updated_last_correct_word
    }


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("corrector", corrector)
graph_builder.add_node("scorer", scorer)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge(START, "corrector")

graph_builder.add_edge("corrector", "scorer")

graph_builder.add_edge("chatbot", END)
graph_builder.add_edge("scorer", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
