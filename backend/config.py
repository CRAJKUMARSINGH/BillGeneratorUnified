"""
Configuration for Flask Backend
Security improvements: Using environment variables instead of hardcoded values
"""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    # Security settings from environment variables
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key-for-dev')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///billgenerator.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-jwt-secret-for-dev')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour default
    
    # Database settings
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    
    # Application settings
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')