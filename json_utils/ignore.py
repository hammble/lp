import json
import os

def save_ignored_users(ignored_users):
    with open("ignored_users.json", "w") as file:
        json.dump(ignored_users, file)

def add_ignore(user_id):
    ignored_users = load_ignored_users()
    if user_id not in ignored_users:
        ignored_users.append(user_id)
        save_ignored_users(ignored_users)

def remove_ignore(user_id):
    ignored_users = load_ignored_users()
    if user_id in ignored_users:
        ignored_users.remove(user_id)
        save_ignored_users(ignored_users)

def load_ignored_users():
    if os.path.exists("ignored_users.json"):
        with open("ignored_users.json", "r") as file:
            return json.load(file)
    else:
        return []