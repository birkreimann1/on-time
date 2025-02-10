import json

def load_json(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

def save_json(data, file_path):
    """Saves data as a JSON file."""
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
