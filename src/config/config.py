import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'l23@+="::##((&&)23432!@)')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Common Database Config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    # SQLite for development
    SQLALCHEMY_DATABASE_URI = os.getenv("POSSGRESS_URL")

class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    # PostgreSQL for production
    SQLALCHEMY_DATABASE_URI = os.getenv("POSSGRESS_URL")

class TestingConfig(Config):
    TESTING = True
    # SQLite for testing (in memory)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name[env]