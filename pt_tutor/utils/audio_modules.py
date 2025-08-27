# import sounddevice as sd
import soundfile as sf
from openai import OpenAI


client = OpenAI()


# def record_audio(filepath, duration, fs, device_index):
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1,  device=device_index)
#     sd.wait()
#     sf.write(filepath, audio, fs)


def transcribe_audio(filepath):
    with open(filepath, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f, 
            response_format='text',
        )
    return transcription


def generate_audio(text, filepath):
    response = client.audio.speech.create(
        model='tts-1',
        voice='alloy',
        input=text,
    )

    with open(filepath, 'wb') as f:
        for chunk in response.iter_bytes():
            f.write(chunk)