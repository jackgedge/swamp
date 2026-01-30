from flask import render_template, request, redirect, url_for
from flask_login import logout_user, login_required, login_user
from werkzeug.security import generate_password_hash
from .helpers import *
from .forms import *
from app.models import *

from app.auth import auth_bp

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = UserRegistrationForm()

    if request.method == "POST":

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
        with Session(engine) as session:
            new_user = User(first_name=first_name, last_name=last_name, esr_number=esr_number, username=username, password_hash=password_hash)
            new_address = Address(email=email)  # Use the correct attribute name
            
            # Associate address with user
            new_user.addresses.append(new_address)
            
            session.add(new_user)  # Adding the user will cascade to addresses
            session.commit()

        return render_template("auth/register_confirm.html", username=username)
    else:
        return render_template("auth/register.html", form=form, title="Register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = UserLoginForm()

    if request.method == "POST":

        username = form.username.data
        password = form.password.data

        def verify_user_login(username, password):
            with Session(engine) as session:
                stmt = select(User).where(User.username == username)
                user = session.scalars(stmt).first()
                if user and check_password_hash(user.password_hash, password):
                    return user  # User object, NOT bool
                return None
                
        user = verify_user_login(username=username, password=password)
        
        if user is None:
            return raise_error(404, "Invalid Credentials")
        else:
            login_user(user)
            return redirect(url_for("main.home"))

    else:
        return render_template("auth/login.html", form=form, title="Log In")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))





