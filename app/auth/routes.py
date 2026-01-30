from flask import render_template, request, redirect, url_for
from flask_login import logout_user, login_required, login_user
from werkzeug.security import generate_password_hash
from .helpers import *
from .forms import UserRegistrationForm, UserLoginForm
from app.models import User, Address
from app.extensions import db
from app.auth import auth_bp

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistrationForm()

    if form.validate_on_submit():

        # Get names
        first_name = form.first_name.data
        last_name = form.last_name.data
        esr_number = form.esr_number.data

        def generate_username(first_name, last_name):
            return first_name[:3].lower() + last_name[:3].lower()

        username = generate_username(first_name, last_name)
        
        email = form.email.data

        # Get password and password_confirm
        password = form.password.data

        # Generate password hash
        password_hash = generate_password_hash(password=password)
        

        # Add to database
        new_user = User(
                first_name=first_name, 
                last_name=last_name, 
                esr_number=esr_number, 
                username=username, 
                password_hash=password_hash)
        new_address = Address(email=email)

        new_user.addresses.append(new_address)
            
        db.session.add(new_user)
        db.session.commit()

        return render_template("auth/register_confirm.html", username=username)
    else:
        return render_template("auth/register.html", form=form, title="Register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("main.home"))
        return raise_error(401, "Invalid Credentials")

    return render_template("auth/login.html", form=form, title="Log In")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))





