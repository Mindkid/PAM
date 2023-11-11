from gtts import gTTS
import os

PAM_SPEECH_FILE_NAME = "pam_speech.mp3"

def playSound(text):
    tts = gTTS(text)
    tts.save(PAM_SPEECH_FILE_NAME)
    os.system("start " + PAM_SPEECH_FILE_NAME)