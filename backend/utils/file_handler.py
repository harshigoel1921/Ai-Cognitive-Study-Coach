import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "../../data/users.json")


def save_user(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_user():
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return {}