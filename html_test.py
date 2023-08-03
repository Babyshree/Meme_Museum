from flask import Blueprint, render_template

html_test = Blueprint("html_test", __name__)


@html_test.route("/base")
def base():
    return render_template("base.html")


@html_test.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")


@html_test.route("/login")
def login():
    return render_template("login.html")

@html_test.route("/about")
def about():
   return render_template("About.html")
