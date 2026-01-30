from flask import Flask, redirect, url_for
from sqlalchemy.orm import Session
from app.extensions import engine
from .extensions import engine, login_manager
from .auth import auth_bp
from .main import main_bp
from app.models import *

from dotenv import load_dotenv
load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with Session(engine) as session:
            return session.get(User, int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    create_tables(engine=engine)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
