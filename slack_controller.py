from sound_player import playSound
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time
import os

USER_NAME = "SpongeBob says: "
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

client = WebClient(token=SLACK_TOKEN)

def send_message(channel_name, message):
    channel_name = channel_name.lower()
    channel_id = get_channel_id(channel_name)
    print("Posting: " + message + " to " + channel_id)
    message = USER_NAME + message
    try:
        client.chat_postMessage(
            channel = channel_id,
            text = message
        )
    except SlackApiError as e:
        print(e)
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'


def read_messages(channel_name, number_of_messages):
    channel_id = get_channel_id(channel_name)
    messages_to_read = []
    try:
        response = client.conversations_history(channel=channel_id)
        messages = response['messages']

        while number_of_messages > 0:
            messages_to_read.append(messages.pop(0))
            number_of_messages = number_of_messages - 1

        for message in messages_to_read:        
            user = get_user_name(message.get('user', 'Unknown User'))
            text = message.get('text', 'No text')
            playSound("User " + user + " wrote " + text)
            time.sleep(10)
    
            
    except SlackApiError as e:
        print(e)
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

def get_channel_id(channel_name):
    channel_name = channel_name.lower()
    response = client.conversations_list()
    channels = response["channels"]

    for channel in channels:
        if channel.get("name") == channel_name:
            return channel.get("id")
    
    raise SlackApiError(message = channel_name + " not found", response = response)

def get_user_name(user_id):
    try:
        response = client.users_info(user=user_id)
        user_info = response['user']
        # Access user information
        return user_info['real_name']
    except SlackApiError as e:
        print(f"Error getting user information: {e.response['error']}")


#print(get_user_name("U0654KY9F6H"))
read_messages("spongebob", 2)
#send_message("spongebob", "test---")
