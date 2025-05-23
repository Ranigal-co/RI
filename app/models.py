# @Ranigal-co
"""
    Модели базы данных
"""
import datetime
from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    theme_preference = db.Column(db.String(10), default='dark')
    avatar = db.Column(db.String(100), default='default-avatar.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', admin={self.is_admin})"


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(128), nullable=False)
    action = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Метод для преобразования объекта в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "key": self.key,
            "action": self.action,
        }

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200))

    def to_dict(self):
        """Метод для преобразования объекта в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.link
        }
    
    def delete(self):
        """Удаляет текущий проект из базы данных"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Project('{self.title}', '{self.link}')"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def to_dict(self):
        """Метод для преобразования объекта в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}')"