from openai import OpenAI
from google.cloud import texttospeech


client = texttospeech.TextToSpeechClient()


def record_audio(audio_recording, filepath): 
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
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(
            text=text
        ),
        voice=texttospeech.VoiceSelectionParams(
            language_code="pt-PT",
            model_name="gemini-2.5-flash-tts",
            name="Sadaltager"
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            pitch=0.0,
            speaking_rate=1.0
        ),
    )

    # with open(filepath, 'wb') as f:
    #     for chunk in response.iter_bytes():
    #         f.write(chunk)

    with open(filepath, "wb") as f:
        f.write(response.audio_content)