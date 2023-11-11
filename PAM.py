from gtts import gTTS
import os

PAM_SPEECH_FILE_NAME = "pam_speach.mp3"

def playSound(text):
    tts = gTTS(text)
    tts.save(PAM_SPEECH_FILE_NAME)
    os.system("start /b " + PAM_SPEECH_FILE_NAME)

playSound("Hello I'm PAM number 4")

