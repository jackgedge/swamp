from sqlalchemy import create_engine
from flask_login import LoginManager

engine = create_engine("sqlite:///instance/test.db", echo=True)

login_manager = LoginManager()
