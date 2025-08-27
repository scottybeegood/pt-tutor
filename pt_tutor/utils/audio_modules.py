import streamlit as st 
# import soundfile as sf
from openai import OpenAI


client = OpenAI()


def record_audio(audio_recording, filepath): 
    # audio_recording = st.audio_input("Record audio")
    with open(filepath, 'wb') as f:
        f.write(audio_recording.getvalue())


def transcribe_audio(filepath):
    with open(filepath, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f, 
            response_format='text',
            language='pt',
        )
    return transcription


def generate_audio(text, filepath):
    response = client.audio.speech.create(
        model='tts-1-hd',
        voice='fable', #  'nova', 'shimmer' are the best alternatives here 
        input=text,
    )

    with open(filepath, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)