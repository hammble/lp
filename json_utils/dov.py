import json
import os

def save_dov_users(dov_users):
    with open("dov_users.json", "w") as file:
        json.dump(dov_users, file)

def add_dov(user_id):
    dov_users = load_dov_users()
    if user_id not in dov_users:
        dov_users.append(user_id)
        save_dov_users(dov_users)

def remove_dov(user_id):
    dov_users = load_dov_users()
    if user_id in dov_users:
        dov_users.remove(user_id)
        save_dov_users(dov_users)

def load_dov_users():
    if os.path.exists("dov_users.json"):
        with open("dov_users.json", "r") as file:
            return json.load(file)
    else:
        return []