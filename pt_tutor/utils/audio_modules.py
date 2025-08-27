# import sounddevice as sd

# import pyaudio
# import wave

import soundfile as sf
from openai import OpenAI


client = OpenAI()


# def record_audio(filepath, duration, fs, device_index):
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1,  device=device_index)
#     sd.wait()
#     sf.write(filepath, audio, fs)


# def record_audio(filepath, duration, fs, device_index):
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1

#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=fs,
#                     input=True,
#                     input_device_index=device_index,
#                     frames_per_buffer=CHUNK)

#     frames = []

#     for _ in range(int(fs / CHUNK * duration)):
#         data = stream.read(CHUNK)
#         frames.append(data)

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     with wave.open(filepath, 'wb') as wf:
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(2)  # 16-bit = 2 bytes
#         wf.setframerate(fs)
#         wf.writeframes(b''.join(frames))


# TODO try Streamlit's built-in audio components: audio_bytes = st.audio_input("Record audio")


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