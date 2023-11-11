from openai import OpenAI
from gtts import gTTS
from commands import Commands
import speech_recognition as sr
import re
import os

PAM_SPEECH_FILE_NAME = "pam_speach.mp3"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def sanitize_command(raw_command):
    return re.sub(r'[^\w]', '', raw_command)

def playSound(text):
    tts = gTTS(text)
    tts.save(PAM_SPEECH_FILE_NAME)
    os.system("start " + PAM_SPEECH_FILE_NAME)
    

#playSound("Hello I'm PAM, i will be you Personal Assistant. Please, what do you need?")

r = sr.Recognizer()

client = OpenAI(
    api_key=OPENAI_API_KEY
)

current_command = Commands.NOTHING

while(current_command != Commands.BYE or current_command != Commands.EXIT):
    with sr.Microphone() as source:
        audio = r.listen(source)
    
    with open("user_input.mp3", "wb") as audio_file:
        audio_file.write(audio.get_raw_data())

    try:
        processed_audio = transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
        if processed_audio == "":
            continue

        print("This is the processed audio: {}", processed_audio)
        current_command = sanitize_command(processed_audio.split()[0].upper())
        print(current_command)
        
    except sr.RequestError as e:
        print("Could not request results from Whisper API")


