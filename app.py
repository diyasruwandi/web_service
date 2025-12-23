from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db
from models.bahan import Bahan 
from controllers.auth_controller import auth
from controllers.user_controller import user_pages
from controllers.admin_controller import admin_pages
from controllers.artikel_controller import article_pages
from controllers.analisis_controller import analysis
from controllers.chatbot_controller import chatbot
from flask_cors import CORS




app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}})


db.init_app(app)

@app.route('/')
# @app.route('/login')
def home():
    # Jika sudah login, arahkan sesuai role
    if "user_id" in session:
        if session["role"] == "admin":
            return redirect(url_for("admin_pages.admin_dashboard"))
        else:
            return redirect(url_for("user_pages.user_dashboard"))

    # Jika belum login, tampilkan login page
    return redirect("/login")


# Register controllers
app.register_blueprint(auth)
app.register_blueprint(user_pages)
app.register_blueprint(admin_pages)
app.register_blueprint(article_pages)
app.register_blueprint(analysis)
app.register_blueprint(chatbot)



if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   app.run(debug=True)