import json
import os

MEMORY_PATH = "data/memory.json"

def _load():
    if not os.path.exists(MEMORY_PATH):
        return {}
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save(data):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def remember(key: str, value):
    data = _load()
    data[key] = value
    _save(data)

def recall(key: str, default=None):
    return _load().get(key, default)