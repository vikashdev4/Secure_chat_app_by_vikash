import json
import os

FILE = "users.json"

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def register(username, password):
    users[username] = password
    with open(FILE, "w") as f:
        json.dump(users, f)

def login(username, password):
    return username in users and users[username] == password