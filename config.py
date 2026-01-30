import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, "instance")
os.makedirs(db_dir, exist_ok=True)  # Auto-creates dir
db_path = os.path.join(db_dir, "test.db")
touch_path = os.path.join(db_dir, "test.db")  # Dummy file
open(touch_path, 'a').close()  # Create empty file

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

