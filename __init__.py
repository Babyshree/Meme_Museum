from os import path, environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "model.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = environ["SECRET_KEY"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # app.config["SQLALCHEMY_ECHO"] = True
    # app.config["SQLALCHEMY_DATABASE_URI"] = f"""sqlite:///{DB_NAME}"""
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"""db2://{environ['USER']}:{environ['PASSWORD']}@{environ['HOST']}:{environ['PORT']}/{environ['DATABASE']};security=ssl;sslcertificate={environ['SSL_CERTIFICATE']}"""
    db.init_app(app)

    from .html_test import html_test
    from .auth import auth
    from .views import views

    app.register_blueprint(html_test, url_prefix="/test")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()
        print("Created Database!")

    # create_database(app)

    login_manager = LoginManager(app=app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).get(int(id))

    return app


def create_database(app: Flask):
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created Database!")
