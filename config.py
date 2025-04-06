# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Основные настройки
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки администратора
    FIRST_ADMIN_USERNAME = os.getenv('FIRST_ADMIN_USERNAME', 'admin')
    FIRST_ADMIN_EMAIL = os.getenv('FIRST_ADMIN_EMAIL', 'admin@example.com')
    FIRST_ADMIN_PASSWORD = os.getenv('FIRST_ADMIN_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Дополнительные настройки для продакшена
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True