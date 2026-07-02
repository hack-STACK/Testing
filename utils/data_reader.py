import json


def load_json(path):
    with open(path, "r") as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)