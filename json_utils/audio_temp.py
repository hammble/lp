import json

audio_messages = {}

def save_audio_messages():
    with open('audio_messages.json', 'w') as f:
        json.dump(audio_messages, f)

def load_audio_messages():
    global audio_messages
    try:
        with open('audio_messages.json', 'r') as f:
            audio_messages = json.load(f)
    except FileNotFoundError:
        pass