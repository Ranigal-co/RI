# @Ranigal-co
"""
    Руты страниц
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Project, Contact, User, ApiKey
from .utils.ready_projects import getProjects
from .utils.utilApi import get
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from flask import abort
from functools import wraps
from flask import abort
from app import db, bcrypt
from flask import current_app
import os
from werkzeug.utils import secure_filename
from config import Config

main_routes = Blueprint('main', __name__)

"""
    Главные руты
"""

@main_routes.route('/')
@main_routes.route('/home')
def index():
    return render_template('index.html')

@main_routes.route("/api", methods=['GET', 'POST'])
def api():
    page = request.args.get('page', 0)
    try:
        page_number = int(page)
    except Exception:
        page_number = 0
    if request.method == "GET":
        api_key = request.args.get('key', 'create')
        if api_key == 'create':
            if not current_user.is_authenticated:
                flash('Для работы с ключами API необходимо авторизироваться', 'warning')
                return redirect(url_for('main.login'))

            values = get(page_number)

            params = {
                "apis": values,
                "page": f"Номер страницы {page_number}",
                "page_number": page_number  # Добавляем номер страницы в контекст
            }
            return render_template('api.html', **params)
        else:
            api_key = ApiKey.query.filter_by(key=api_key).first()
            try:
                action = api_key.action
                if action == 1:
                    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
                    return jsonify({
                        'success': True,
                        'contacts': [contact.to_dict() for contact in contacts]
                    })
                return jsonify({
                    'success': False,
                    'reason': "Wrong action in API key"
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'reason': "Wrong API key",
                    'error': str(e)
                }), 500

    action = request.form.get("action")
    if action == "next_page":
        return redirect(url_for("main.api") + f"?page={page_number + 1}")
    elif action == "prev_page":
        return redirect(url_for("main.api") + f"?page={max(0, page_number - 1)}")
    elif action == "open_link":
        link = request.form.get("data_link")
        return redirect(url_for("main.api") + f"?page={link}")


@main_routes.route('/about')
def about():
    return render_template('about.html')

@main_routes.route('/projects', methods=["GET", "POST"])
def projects():
    page = request.args.get('page', 0)
    try:
        page_number = max(0, int(page))
    except ValueError:
        page_number = 0
        
    values = getProjects(page_number)
    
    if request.method == "GET":
        params = {
            "projects": values,
            "page": f"Номер страницы {page_number}",
            "page_number": page_number  # Добавляем номер страницы в контекст
        }
        return render_template('projects.html', **params)
        
    action = request.form.get("action")
    if action == "next_page":
        return redirect(url_for("main.projects") + f"?page={page_number + 1}")
    elif action == "prev_page":
        return redirect(url_for("main.projects") + f"?page={max(0, page_number - 1)}")
    elif action == "open_link":
        link = request.form.get("data_link")
        return redirect(url_for("main.project") + f"?link={link}")

@main_routes.route('/contact', methods=['GET', 'POST'])
def contact():
    if not current_user.is_authenticated:
        flash('Для отправки сообщения необходимо авторизоваться', 'warning')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        message = request.form.get('message')

        if not message:
            flash('Сообщение не может быть пустым', 'error')
            return redirect(url_for('main.contact'))

        try:
            new_contact = Contact(
                name=current_user.username,
                email=current_user.email,
                message=message
            )
            db.session.add(new_contact)
            db.session.commit()
            flash('Сообщение успешно отправлено!', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'error')
    return render_template('contact.html')

"""
    Функции админа
"""

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main_routes.route('/admin/api/add', methods=["GET", "POST"])
@admin_required
def add_api():
    if request.method == "GET":
        return render_template("admin/add_api.html")
    title = request.form.get('title')
    key = request.form.get('key')
    action = request.form.get('action')

    if not all([title, key, action]):
        flash('Все поля обязательны для заполнения', 'error')
        return redirect(url_for('main.add_api'))

    try:
        new_api = ApiKey(title=title, key=key, action=int(action))
        db.session.add(new_api)
        db.session.commit()
        flash('API ключ успешно добавлен!', 'success')
        return redirect(url_for('main.api'))
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка: {str(e)}', 'error')
    return render_template('admin/add_api.html')

@main_routes.route('/admin/contacts')
@admin_required
def view_contacts():
    """Отображение всех контактов в HTML"""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@main_routes.route('/admin/contacts/<int:contact_id>')
@admin_required
def view_contact(contact_id):
    """Отображение конкретного контакта"""
    contact = Contact.query.get_or_404(contact_id)
    return render_template('admin/contact_detail.html', contact=contact)

@main_routes.route('/admin/projects/add', methods=['GET', 'POST'])
@admin_required
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        if not all([title, description, link]):
            flash('Все поля обязательны для заполнения', 'error')
            return redirect(url_for('main.add_project'))

        try:
            new_project = Project(title=title, description=description, link=link)
            db.session.add(new_project)
            db.session.commit()
            flash('Проект успешно добавлен!', 'success')
            return redirect(url_for('main.projects'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {str(e)}', 'error')
    
    return render_template('admin/add_project.html')

"""
    Взаимодействиея с профилем
"""

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
    admin_exists = User.query.filter_by(is_admin=True).first() is not None
    return render_template('user/profile.html', 
                         user=current_user,
                         admin_exists=admin_exists)

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_routes.route('/make_admin', methods=['POST'])
@login_required
def make_admin():
    # Проверяем, есть ли уже администраторы
    if User.query.filter_by(is_admin=True).first():
        flash('Администратор уже существует', 'warning')
        return redirect(url_for('main.profile'))
    
    username = request.form.get('admin_username')
    
    # Проверяем, что текущий пользователь пытается назначить самого себя
    if username != current_user.username:
        flash('Вы можете назначить только себя администратором', 'danger')
        return redirect(url_for('main.profile'))
    
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_admin = True
        db.session.commit()
        flash(f'Пользователь {username} теперь администратор', 'success')
    else:
        flash('Пользователь не найден', 'danger')
    
    return redirect(url_for('main.profile'))

@main_routes.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

@main_routes.route('/set_theme', methods=['POST'])
@login_required
def set_theme():
    theme = request.json.get('theme')
    if theme in ['light', 'dark']:
        current_user.theme_preference = theme
        db.session.commit()
        return jsonify({
            'success': True,
            'images': {
                'header_bg': url_for('static', filename=f'images/anime-bg-{theme}.jpg'),
                'logo': url_for('static', filename=f'images/logo-{theme}.png')
            }
        })
    return jsonify({'success': False}), 400

def allowed_file(filename):
    """Проверка разрешенных расширений файлов"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_routes.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'file' not in request.files:
        flash('Файл не выбран', 'error')
        return redirect(url_for('main.profile'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Не выбран файл', 'error')
        return redirect(url_for('main.profile'))
    
    if not file or not allowed_file(file.filename):
        flash('Недопустимый формат файла', 'error')
        return redirect(url_for('main.profile'))
    
    try:
        # Создаем папку avatars если её нет
        avatars_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars')
        os.makedirs(avatars_dir, exist_ok=True)
        
        # Генерируем имя файла
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"user_{current_user.id}.{ext}"
        filepath = os.path.join(avatars_dir, filename)
        
        # Сохраняем файл
        file.save(filepath)
        
        # Обновляем БД
        current_user.avatar = filename
        db.session.commit()
        flash('Аватар успешно обновлен!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Ошибка загрузки аватара: {str(e)}")
        flash('Ошибка при загрузке аватара', 'error')
    
    return redirect(url_for('main.profile'))

@main_routes.route('/admin/projects/delete/<int:project_id>', methods=['POST'])
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Проект успешно удален!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении проекта: {str(e)}', 'error')
    return redirect(url_for('main.projects'))