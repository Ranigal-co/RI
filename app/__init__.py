# @Ranigal-co
"""
    Логика и все необходимое для запуска сервера
    Чтобы сделать себя админом создай файл .env и напиши там это:
    SECRET_KEY=сгенирируй его в tests/__init__.py
    FIRST_ADMIN_USERNAME=Имя
    FIRST_ADMIN_EMAIL=Почта
    FIRST_ADMIN_PASSWORD=Пароль
    И потом на сайте сможешь зайти в админку
"""

from flask import Flask
from app.extensions import db, bcrypt, login_manager
from .utils.ready_projects import registry
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    """Главный объект сервера"""
    app = Flask(__name__)
    
    # Загружаем конфигурацию из класса Config
    app.config.from_object(config_class)
    
    # Инициализация расширений
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
        create_first_admin(app)

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app

def create_first_admin(app):
    """Создает первого администратора"""
    from app.models import User
    
    if not User.query.filter_by(is_admin=True).first():
        if not app.config.get('FIRST_ADMIN_PASSWORD'):
            print("Пароль администратора не задан в .env")
            return
            
        if User.query.filter_by(username=app.config['FIRST_ADMIN_USERNAME']).first():
            print("Пользователь с таким именем уже существует")
            return
            
        admin = User(
            username=app.config['FIRST_ADMIN_USERNAME'],
            email=app.config['FIRST_ADMIN_EMAIL'],
            password=bcrypt.generate_password_hash(app.config['FIRST_ADMIN_PASSWORD']).decode('utf-8'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

        registry()

        print(f"Создан первый администратор: {app.config['FIRST_ADMIN_USERNAME']}")
        print("Проекты загружены!")
