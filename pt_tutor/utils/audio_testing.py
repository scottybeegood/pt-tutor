import pt_tutor.utils.audio_modules as am

duration = 5
fs = 48000
device_index = 0

am.record_audio('pt_tutor/data/audio/question.wav', duration, fs, device_index)

transcription = am.transcribe_audio('pt_tutor/data/audio/question.wav')
print(transcription)

am.generate_audio(transcription, 'pt_tutor/data/audio/answer.mp3')
