import streamlit as st 
import os
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID")

llm = OpenAI(api_key=openai_api_key, organization=openai_org_id)


st.set_page_config(layout="wide", page_title="Fala Português!")

st.write("## Fala Português!")

st.sidebar.radio(
    "Select your name or add a new one:",
    key="visibility",
    options=["Scott", "Bianca", "New user"],
)

st.sidebar.text_input(
    "Select the topic you'd like to discuss:",
    "eg, Dining out",
    # key=["Dining out"],
)

col1, col2 = st.columns(2)

col1.write("Fala aqui...")


col2.write("Feedback on responses here...")


