import os
import json

def save_message(chatroom, username, message):
    history_file = f"history_{chatroom}.json"
    messages = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            messages = json.load(file)
    messages.append(f"{username}: {message}")
    with open(history_file, 'w') as file:
        json.dump(messages, file)

def get_messages(chatroom):
    history_file = f"history_{chatroom}.json"
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []
