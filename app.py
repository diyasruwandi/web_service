from flask import Flask, render_template, session, redirect
from config import Config
from models import db
from controllers.auth_controller import auth
from controllers.user_controller import user_pages
from controllers.admin_controller import admin_pages
from controllers.artikel_controller import article_pages


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)

@app.route('/')
@app.route('/login')
def home():
    # Jika sudah login, arahkan sesuai role
    if "user_id" in session:
        if session["role"] == "admin":
            return redirect("/admin/dashboard")
        else:
            return redirect("/user/dashboard")

    # Jika belum login, tampilkan login page
    return render_template('login.html')


# Register controllers
app.register_blueprint(auth)
app.register_blueprint(user_pages)
app.register_blueprint(admin_pages)
app.register_blueprint(article_pages)


if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   app.run(debug=True)