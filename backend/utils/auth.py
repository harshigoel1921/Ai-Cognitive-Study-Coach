import json
import os

FILE = os.path.join(os.path.dirname(__file__), "../../data/auth.json")


def load_users():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def register_user(username, password):
    users = load_users()

    if username in users:
        return False

    users[username] = password
    save_users(users)
    return True


def login_user(username, password):
    users = load_users()

    if username in users and users[username] == password:
        return True

    return False