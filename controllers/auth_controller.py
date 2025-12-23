from flask import Blueprint, render_template, request, redirect, session, url_for
from models.user import User, db, bcrypt

auth = Blueprint("auth", __name__)

# LOGIN
@auth.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["role"] = user.role.value

            if user.role.value == "admin":
                return redirect(url_for("admin_pages.admin_dashboard"))
            else:
                return redirect(url_for("user_pages.user_dashboard"))

        error = "Email atau password salah"

    return render_template("login.html", error=error)


# REGISTER
@auth.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode()

         # Cek apakah email sudah terdaftar
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error = "Email sudah digunakan, silakan pakai email lain."
            return render_template("register.html", error=error)

        new_user = User(email=email, password=password, role="user")
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html", error=error)


@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
