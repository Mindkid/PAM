from sound_player import playSound
from commands import Commands
from commands import process_commands
from commands import sanitize_command
from scipy.io.wavfile import write
from openai import OpenAI
import sounddevice as sd
import os

USER_SPEECH_FILE_NAME = "user_speech.mp3"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Recording settings
FREQUENCY = 48000 
DURANTION = 5



def getCommand(userCommand):
    try:
        return Commands[userCommand]
    except:
        return Commands.NOTHING

playSound("Hello I'm PAM, i will be you Personal Assistant. Please, what do you need?")

client = OpenAI()

current_command = Commands.NOTHING
processed_audio = ""

while(current_command != Commands.BYE and current_command != Commands.EXIT):
    print("say your comamnd")
    recording = sd.rec(int(DURANTION * FREQUENCY), 
                   samplerate=FREQUENCY, channels=2)
    sd.wait()

    write(USER_SPEECH_FILE_NAME, FREQUENCY, recording)
    
    user_request = open(USER_SPEECH_FILE_NAME, "rb")
    processed_audio = client.audio.transcriptions.create(model="whisper-1", file=user_request, response_format="text").strip()
    user_request.close()
    
    
    if processed_audio == "":
        continue

    print("processed data: {}", processed_audio)

    user_comands = processed_audio.split()
    current_command = getCommand(sanitize_command(user_comands.pop(0).upper()))
    process_commands(current_command, user_comands)
 
playSound("Bye and I hope that I've helped")
