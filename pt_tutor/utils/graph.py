import os
import pandas as pd
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


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

llm = ChatOpenAI(
    api_key=openai_api_key,
    organization=openai_org_id,
    model="gpt-4o",
    temperature=0.8
)


class State(TypedDict):
    messages: Annotated[list, add_messages]
    core_convo: Annotated[list, add_messages]
    corrections: Annotated[list, add_messages]
    correct_words: dict


topic = "Dining out" # TODO: make into a parameter
language = "European Portuguese" # TODO: make into a parameter


def chatbot(state: State):
    system_message = chatbot_instructions.format(topic=topic, language=language)
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
    # user_message = 'Aquilo está bem. Eu gosto de comer lá. Mas eu não gosto de comer cá.'
    corrector_message = next(
        (m.content for m in reversed(state['corrections']) if isinstance(m, AIMessage)),
        None
    )
    # corrector_message = 'Essa está mal. Eu gosto de comer x. Mas eu x gosto de comer y.'

    state.setdefault("correct_words", {})

    for user_word in user_message.split():
        if user_word in corrector_message.split():
            if user_word in state["correct_words"]:
                state["correct_words"][user_word] += 1
            else:
                state["correct_words"][user_word] = 1

    print (f'last user message words: {user_message.split()}')
    print (f'last corrector message words: {corrector_message.split()}')
    # print(state)

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

