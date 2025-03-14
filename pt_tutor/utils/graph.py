import os
import pandas as pd
import re
from dotenv import load_dotenv
from pydantic import BaseModel

from typing import Annotated, Literal

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from langgraph.types import Command
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import InjectedState, ToolNode
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.tools import tool

from utils.instructions import (
    chatbot_instructions,
    corrector_instructions
)
from utils.functions import (
    clean_message,
    # import_gsheet_tab
)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

llm = ChatOpenAI(
    api_key=openai_api_key,
    organization=openai_org_id,
    model="gpt-4o-mini",
    temperature=0.8
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    core_convo: Annotated[list, add_messages]
    corrections: Annotated[list, add_messages]
    topic_vocab: set #list
    correct_words: dict
    mastered_words: set #list
    last_mastered_word: str
    topic: str 


def chatbot(state: State):
    topic = state["topic"]
    mastered_words = state["mastered_words"]

    system_message = chatbot_instructions.format(topic=topic, mastered_words=mastered_words)
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

    state.setdefault("correct_words", {})

    for user_word in corrector_message.split():
        if user_word in user_message.split() and user_word in state["topic_vocab"]:
            # update correct_words dict
            if user_word in state["correct_words"]:
                state["correct_words"][user_word] += 1
                if state["correct_words"][user_word] >= 3:
                    state["mastered_words"].add(user_word)
                    state["last_mastered_word"] = user_word
            else:
                state["correct_words"][user_word] = 1
                
            # paint that user_word in corrector_message green
        # else paint that user_word in corrector_message red

    # print(f'topic vocab words: {state["topic_vocab"]}')
    # print (f'last user message words: {user_message.split()}')
    # print (f'last corrector message words: {corrector_message.split()}')

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
