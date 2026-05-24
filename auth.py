import hashlib, json, os

FILE = "users.json"

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def hash_password(p):
    if not p:
        return ""
    return hashlib.sha256(p.encode()).hexdigest()

def register(u, p):
    users[u] = hash_password(p)
    with open(FILE, "w") as f:
        json.dump(users, f)

def login(u, p):
    return u in users and users[u] == hash_password(p)