# @Ranigal-co
"""
    Здесь находятся все страницы
    Рендер html из папки templates для соотвествующей страницы

    p.s. base.html это файл-основа для других html
"""

from flask import Blueprint, render_template

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index(): # Приветсвенная страница
    return render_template('index.html')

@main_routes.route('/about')
def about(): # О нас 
    return render_template('about.html') # 

@main_routes.route('/projects')
def projects(): # Наши проекты, ссылки на них/работающие протипы на сайте(дейлик или ещё что)
    return render_template('projects.html')

@main_routes.route('/contact')
def contact(): # Наши контакты
    return render_template('contact.html')