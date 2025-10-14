import os
import streamlit as st

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
    model="gpt-4o-mini", # "gpt-5"  <-- too verbose 
    temperature=0.7 # 1.0
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    core_convo: Annotated[list, add_messages]
    corrections: Annotated[list, add_messages]
    correct_count: dict
    last_correct_word: str
    topic: str 


def chatbot(state: State):
    topic = state["topic"]
    all_vocab = set(state["correct_count"].keys())
    correct_vocab = {word for word, count in state["correct_count"].items() if count > 0}

    system_message = chatbot_instructions.format(topic=topic, 
                                                 all_vocab=all_vocab,
                                                 correct_vocab=correct_vocab)
    response = llm.invoke([SystemMessage(content=system_message)]+state["messages"])

    state["messages"] = [response]
    state["core_convo"] = [response] 

    return state


def corrector(state: State):
    user_message = next(
        (m.content for m in reversed(state['core_convo']) if isinstance(m, HumanMessage)),
        None
    )

    system_message = corrector_instructions.format(user_message=user_message)
    response = llm.invoke([SystemMessage(content=system_message)]+state["messages"])

    state["messages"] = [response]
    state["corrections"] = [response]

    return state


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

    # state.setdefault("correct_count", {})

    for user_word in corrector_message.split():
        if user_word in user_message.split() and user_word in state["correct_count"].keys():
            state["correct_count"][user_word] += 1
            state["last_correct_word"] = user_word
 
    return state


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("corrector", corrector)
graph_builder.add_node("scorer", scorer)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "corrector")
graph_builder.add_edge("corrector", "scorer")
graph_builder.add_edge("chatbot", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
