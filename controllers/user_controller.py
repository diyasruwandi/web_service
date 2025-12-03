from flask import Blueprint, session, redirect, render_template,  request, jsonify
from models.artikel import Article 
from mesin_chatbot import get_bot_response

user_pages = Blueprint('user_pages', __name__)

@user_pages.route('/user/dashboard', methods=['GET'])
def user_dashboard():

    articles = Article.query.all()   # ambil semua artikel

    return render_template(
        "user/userDashboard.html",
        articles=articles             # kirim ke template
    )

@user_pages.route('/chatbot', methods=['POST'])
def chatbot_api():
    user_message = request.json.get("message")
    response = get_bot_response(user_message)
    return jsonify({"response": response})
