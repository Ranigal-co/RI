# @Ranigal-co
"""
    Руты страниц
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Project, Contact
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from flask import abort
from app import db

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
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