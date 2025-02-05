from flask import Blueprint, request, redirect, url_for, session, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import add_user, get_users, get_user_by_id, update_password, delete_user

admin_users_bp = Blueprint('admin_users', __name__)

@admin_users_bp.route('/admin/add_user', methods=['POST'])
def add_user_route():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == "on"
    
    if get_user_by_id(db, username):
        return "Ошибка: Пользователь уже существует", 400
    
    if add_user(db, username, password, is_admin):
        return redirect(url_for('admin_main.admin'))
    return "Ошибка при добавлении пользователя", 500

@admin_users_bp.route('/admin/remove_user', methods=['POST'])
def remove_user():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    user_id = request.form.get('user_id')
    delete_user(db, user_id)
    
    return redirect(url_for('admin_main.admin'))

@admin_users_bp.route('/admin/change_password', methods=['POST'])
def change_password():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    
    if not get_user_by_id(db, user_id):
        return "Ошибка: Пользователь не найден", 404
    
    update_password(db, user_id, new_password)
    return redirect(url_for('admin_main.admin'))