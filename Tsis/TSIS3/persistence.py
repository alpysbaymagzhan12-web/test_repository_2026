import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    return os.path.join(BASE_DIR, filename)

def load_json(filename, default):
    path = get_path(filename)
    if not os.path.exists(path): return default
    with open(path, "r") as f:
        try: return json.load(f)
        except: return default

def save_json(filename, data):
    with open(get_path(filename), "w") as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score):
    scores = load_json("leaderboard.json", [])
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    save_json("leaderboard.json", scores)