import os
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from google.cloud import (
    speech, 
    texttospeech
)
from google.oauth2 import service_account
from langchain_core.messages import SystemMessage

from utils.instructions import transcript_refiner_instructions


credentials = service_account.Credentials.from_service_account_info(dict(st.secrets["google_cloud"]))
stt_client = speech.SpeechClient(credentials=credentials)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
openai_org_id = os.getenv("OPENAI_ORG_ID") or st.secrets.get("OPENAI_ORG_ID")

llm = ChatOpenAI(
    api_key=openai_api_key,
    organization=openai_org_id,
    model="gpt-3.5-turbo",
    temperature=1.0,
)


def record_audio(audio_recording, filepath): 
    with open(filepath, 'wb') as f:
        f.write(audio_recording.getvalue())


def transcribe_and_refine_audio(filepath):
    with open(filepath, 'rb') as f:
        audio_content = f.read()

    response = stt_client.recognize(
        audio=speech.RecognitionAudio(content=audio_content),
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="pt-PT",
            model="default",
        ),
    )

    transcription = " ".join([result.alternatives[0].transcript for result in response.results])

    system_message = transcript_refiner_instructions.format(transcription=transcription)
    response = llm.invoke([SystemMessage(content=system_message)])
    transcription_refined = response.content 

    return transcription_refined


def generate_audio(text, filepath):
    response = tts_client.synthesize_speech(
        input=texttospeech.SynthesisInput(
            text=text
        ),
        voice=texttospeech.VoiceSelectionParams(
            language_code="pt-PT",
            model_name="gemini-2.5-flash-tts",
            name=st.session_state.voice_model,
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            pitch=0.0,
            speaking_rate=1.0
        ),
    )

    with open(filepath, "wb") as f:
        f.write(response.audio_content)
