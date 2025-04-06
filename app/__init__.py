# @Ranigal-co
"""
    Логика и все необходимое для запуска сервера
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    """Главный объект сервера"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dJSBDBkBKJbKJFBkBkJBfKBFfKJdbksjf'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'

    from app.models import Project, Contact, User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app