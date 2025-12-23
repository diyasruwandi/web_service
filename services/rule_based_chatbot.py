import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_DIR, "rules.json")

def load_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["rules"], data["fallback"]

RULES, FALLBACK = load_rules()

def get_bot_response(user_message):
    user_message = user_message.lower()

    for rule in RULES:
        for keyword in rule["keywords"]:
            if keyword in user_message:
                return rule["response"]

    return None
