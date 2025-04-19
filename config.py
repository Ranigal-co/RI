# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Основные настройки
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки администратора
    FIRST_ADMIN_USERNAME = os.getenv('FIRST_ADMIN_USERNAME', 'admin')
    FIRST_ADMIN_EMAIL = os.getenv('FIRST_ADMIN_EMAIL', 'admin@example.com')
    FIRST_ADMIN_PASSWORD = os.getenv('FIRST_ADMIN_PASSWORD')

    UPLOAD_FOLDER = BASE_DIR / 'app' / 'static' / 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Дополнительные настройки для продакшена
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True