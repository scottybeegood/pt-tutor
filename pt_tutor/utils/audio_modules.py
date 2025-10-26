import streamlit as st
from google.cloud import (
    speech, 
    texttospeech
)
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_info(dict(st.secrets["google_cloud"]))
stt_client = speech.SpeechClient(credentials=credentials)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)


def record_audio(audio_recording, filepath): 
    with open(filepath, 'wb') as f:
        f.write(audio_recording.getvalue())


def transcribe_audio(filepath):
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

    return transcription


def generate_audio(text, filepath):
    response = tts_client.synthesize_speech(
        input=texttospeech.SynthesisInput(
            text=text
        ),
        voice=texttospeech.VoiceSelectionParams(
            language_code="pt-PT",
            model_name="gemini-2.5-flash-tts",
            name="Sadaltager",
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            pitch=0.0,
            speaking_rate=1.0
        ),
    )

    with open(filepath, "wb") as f:
        f.write(response.audio_content)
