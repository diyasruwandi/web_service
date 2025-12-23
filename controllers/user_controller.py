from flask import Blueprint, session, redirect, render_template,  request, jsonify, url_for
from models.artikel import Article 

user_pages = Blueprint('user_pages', __name__)

@user_pages.route('/user/dashboard', methods=['GET'])
def user_dashboard():

    articles = Article.query.all()   # ambil semua artikel

    return render_template(
        "user/userDashboard.html",
        articles=articles             # kirim ke template
    )