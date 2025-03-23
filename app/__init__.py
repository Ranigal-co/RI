# @Ranigal-co
"""
    Логика и все необходимое для запуска сервера
"""

from flask import Flask
# from config import Config # config.py как settings, потом подлючим


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)

    from app.routes import main_routes # из routes.py получаем все страницы
    app.register_blueprint(main_routes)
     
    return app