from flask import render_template
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models import User

def verify_user_login(username: str, password: str) -> bool:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return True
        return False
        
def raise_error(error_code, error_message):
    return render_template("main/error.html", error_message=error_message, error_code=error_code), error_code
