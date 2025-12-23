from flask import Blueprint, request, jsonify
from services.rule_based_chatbot import get_bot_response
from services.gemini_chatbot import get_gemini_response

chatbot = Blueprint("chatbot", __name__)

SYSTEM_PROMPT = """
Kamu adalah chatbot kesehatan makanan.
Jawab hanya tentang:
- kandungan makanan
- bahan alami dan sintetis
- keamanan makanan
- aplikasi ini
"""

@chatbot.route("/chatbot", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # Rule-based dulu
    rule_answer = get_bot_response(user_message)
    if rule_answer:
        return jsonify({
            "reply": rule_answer,
            "source": "rule-based"
        })

    # Kalau tidak ada jawaban, pakai Gemini
    prompt = f"{SYSTEM_PROMPT}\nUser: {user_message}\nChatbot:"
    gemini_answer = get_gemini_response(prompt)

    return jsonify({
        "reply": gemini_answer,
        "source": "gemini"
    })