from flask import render_template
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
from app.extensions import engine
from app.models import User

def verify_user_login(username: str, password: str) -> bool:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        user = session.scalars(stmt).first()
        if user is None:
            return False # User not found
        
        # Verify password against password hash
        if check_password_hash(user.password_hash, password):
            return True
        else:
            return False
        
def raise_error(error_code, error_message):
    return render_template("main/error.html", error_message=error_message, error_code=error_code), error_code
