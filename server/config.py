# server/config.py

import os

class Config:
    # Set the secret key for sessions
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///skill_swap.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
