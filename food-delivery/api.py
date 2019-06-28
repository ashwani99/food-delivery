from dotenv import load_dotenv
from app import app, db


load_dotenv(verbose=True)

with app.app_context():
    db.create_all()
