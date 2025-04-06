# @Ranigal-co
"""
    Руты страниц
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Project, Contact, User
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from flask import abort
from app import db, bcrypt

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@main_routes.route('/home')
def index():
    return render_template('index.html')

@main_routes.route('/about')
def about():
    return render_template('about.html')

@main_routes.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@main_routes.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('main.contact'))

        try:
            new_contact = Contact(name=name, email=email, message=message)
            db.session.add(new_contact)
            db.session.commit()
            flash('Сообщение успешно отправлено!', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'error')
    return render_template('contact.html')

@main_routes.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Получение всех контактов в формате JSON"""
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify({
            'success': True,
            'contacts': [contact.to_dict() for contact in contacts]
        })
    except SQLAlchemyError as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main_routes.route('/admin/contacts')
def view_contacts():
    """Отображение всех контактов в HTML"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@main_routes.route('/admin/contacts/<int:contact_id>')
def view_contact(contact_id):
    """Отображение конкретного контакта"""
    contact = Contact.query.get_or_404(contact_id)
    return render_template('admin/contact_detail.html', contact=contact)

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Проверка совпадения паролей
        if password != confirm_password:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('main.register'))
        
        # Проверка уникальности username и email
        if User.query.filter_by(username=username).first():
            flash('Это имя пользователя уже занято', 'danger')
            return redirect(url_for('main.register'))
        if User.query.filter_by(email=email).first():
            flash('Этот email уже используется', 'danger')
            return redirect(url_for('main.register'))
        
        # Хеширование пароля
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Создание пользователя
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Аккаунт создан! Теперь вы можете войти', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('user/register.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.profile'))
        else:
            flash('Вход не выполнен. Проверьте имя пользователя и пароль', 'danger')
    
    return render_template('user/login.html')

@main_routes.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html', user=current_user)

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Защищенный маршрут - пример
@main_routes.route('/protected')
@login_required
def protected():
    return "Это защищенная страница, доступная только авторизованным пользователям!"