import re
from enum import Enum
from slack_controller import send_message, read_messages
from word2number import w2n

class Commands(Enum):
    NOTHING = 0
    BYE = 1
    EXIT = 2
    OPEN = 3
    SEND = 4
    WRITE = 5
    READ = 6

def process_commands(command, sub_command):
    if(is_invalid_sub_command(sub_command)):
        return
    
    match command:
        case Commands.OPEN:
            print("opening the email")
        case Commands.SEND:
            sub_command.remove("to")
            send_message(sanitize_command(sub_command.pop()), " ".join(sub_command))
        case Commands.READ:
            sub_command.remove("from")
            read_messages(sanitize_command(sub_command.pop()), w2n.word_to_num(sub_command.pop(0)))
            print("sending the email")
        

# SEND heloooo to Claudia Valente

def is_invalid_sub_command(sub_command):
    return len(sub_command) < 2

def sanitize_command(raw_command):
    return re.sub(r'[^\w]', '', raw_command)