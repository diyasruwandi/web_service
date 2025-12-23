from flask import Blueprint, session, redirect, render_template, request, url_for
from models.artikel import Article
from models import db

admin_pages = Blueprint('admin_pages', __name__)


@admin_pages.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    return render_template ("/admin/adminDashboard.html")

@admin_pages.route('/admin/articles')
def admin_articles():
    articles = Article.query.all()
    return render_template('admin/artikel.html', articles=articles)


#  Tambah Artikel
@admin_pages.route('/admin/articles/add', methods=['GET', 'POST'])
def admin_add_article():
    if request.method == 'POST':
        new_data = Article(
            title=request.form['title'],
            image_url=request.form['image_url'],
            description=request.form['description'],
            news_link=request.form['news_link']
        )
        db.session.add(new_data)
        db.session.commit()

        return redirect(url_for('admin_pages.admin_articles'))

    return render_template('admin/tambah_artikel.html')

@admin_pages.route("/admin/articles/edit/<int:id>", methods=["GET", "POST"])
def edit_article(id):
    article = Article.query.get_or_404(id)

    if request.method == "POST":
        article.title = request.form["title"]
        article.image_url = request.form["image_url"]
        article.description = request.form["description"]
        article.news_link = request.form["news_link"]

        db.session.commit()
        return redirect("/admin/articles")

    return render_template("admin/edit_artikel.html", article=article)


@admin_pages.route("/admin/articles/delete/<int:id>", methods=["POST"])
def delete_article(id):
    article = Article.query.get_or_404(id)

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('admin_pages.admin_articles'))
