from flask import render_template, redirect, url_for
from flask_login import login_required
from app.auth.helpers import *
from app.models import *
from app.main import main_bp
from app.main.forms import *

@main_bp.route("/")
def index():
    return redirect(url_for("auth.login"))

@main_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("main/home.html", title="Home")
