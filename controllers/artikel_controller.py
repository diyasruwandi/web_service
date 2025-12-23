from flask import Blueprint, request, jsonify, session
from models.artikel import Article
from models import db

article_pages = Blueprint("article_pages", __name__)

# Helper: hanya admin yang boleh mengakses endpoint ini
def admin_only():
    return session.get("role") == "admin"

# CREATE ARTICLE
@article_pages.route("/admin/article", methods=["POST"])
def create_article():
    if not admin_only():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    new_article = Article(
        title=data["title"],
        image_url=data.get("image_url"),
        description=data["description"],
        news_link=data.get("news_link")
    )

    db.session.add(new_article)
    db.session.commit()

    return jsonify({"message": "Article created successfully"}), 201


# GET ALL ARTICLES
@article_pages.route("/admin/article", methods=["GET"])
@article_pages.route("/articles", methods=["GET"])  # user juga butuh
def get_articles():
    articles = Article.query.all()

    result = []
    for a in articles:
        result.append({
            "id": a.id,
            "title": a.title,
            "image_url": a.image_url,
            "description": a.description,
            "news_link": a.news_link,
            "created_at": a.created_at
        })

    return jsonify(result)


# GET ONE ARTICLE
@article_pages.route("/admin/article/<int:id>", methods=["GET"])
def get_article(id):
    if not admin_only():
        return jsonify({"error": "Unauthorized"}), 401

    a = Article.query.get_or_404(id)

    return jsonify({
        "id": a.id,
        "title": a.title,
        "image_url": a.image_url,
        "description": a.description,
        "news_link": a.news_link,
    })


# UPDATE ARTICLE
@article_pages.route("/admin/article/<int:id>", methods=["PUT"])
def update_article(id):
    if not admin_only():
        return jsonify({"error": "Unauthorized"}), 401

    a = Article.query.get_or_404(id)
    data = request.json

    a.title = data.get("title", a.title)
    a.image_url = data.get("image_url", a.image_url)
    a.description = data.get("description", a.description)
    a.news_link = data.get("news_link", a.news_link)

    db.session.commit()

    return jsonify({"message": "Updated successfully"})


# DELETE ARTICLE
@article_pages.route("/admin/article/<int:id>", methods=["POST"])
def delete_article(id):
    if not admin_only():
        return jsonify({"error": "Unauthorized"}), 401

    a = Article.query.get_or_404(id)

    db.session.delete(a)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})
