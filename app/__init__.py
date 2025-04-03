# @Ranigal-co
"""
    Логика и все необходимое для запуска сервера
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Главный объект сервера"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dJSBDBkBKJbKJFBkBkJBfKBFfKJdbksjf'

    # Конфигурация базы данных (замените на свою)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.models import Project, Contact

    with app.app_context():
        db.create_all()

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app