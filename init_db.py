import os
from dotenv import load_dotenv

# Set default env vars if not exist
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'dev-secret-key'
if not os.environ.get('FERNET_KEY'):
    from cryptography.fernet import Fernet
    os.environ['FERNET_KEY'] = Fernet.generate_key().decode()

from backend.app import create_app
from backend.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
