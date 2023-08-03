from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/about")
def about():
   return render_template("About.html",user=current_user)

@auth.route("/Home")
def home():
    return render_template("home.html",user=current_user)

@auth.route("/contact")
def contact():
    return render_template("contact.html",user=current_user)



@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        pwd = request.form.get("pass")
        pass_conf = request.form.get("pass_conf")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif pwd != pass_conf:
            flash("Passwords don't match.", category="error")
        elif len(pwd) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(pwd, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign-up.html", user=current_user)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = db.session.query(User).filter_by(email=request.form.get("email")).first()

        if user:
            if check_password_hash(user.password, request.form.get("pass")):
                login_user(user, remember=True)
                flash(
                    f"Logged in as {current_user.name.capitalize()}!",
                    category="success",
                )
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password!", category="error")
        else:
            flash("Incorrect Email!", category="error")

    return render_template("login.html", user=current_user)




@auth.route("/logout")
@login_required
def logout():
    flash(
        f"{current_user.name.capitalize()} Logged out successfully!", category="success"
    )
    logout_user()
    return redirect(url_for("auth.login"))



