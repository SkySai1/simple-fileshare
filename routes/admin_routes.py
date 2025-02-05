from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from sqlalchemy.orm import Session
from utils.db_utils import get_db, add_user, get_users, grant_access, update_password, delete_user, revoke_access, get_user_files
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    users = get_users(db)
    files = os.listdir("./files")
    
    return render_template('admin.html', users=users, files=files)

@admin_bp.route('/admin/add_user', methods=['POST'])
def add_user_route():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == "on"
    
    if add_user(db, username, password, is_admin):
        return redirect(url_for('admin.admin'))
    return "Ошибка: Пользователь уже существует", 400

@admin_bp.route('/admin/remove_user', methods=['POST'])
def remove_user():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    user_id = request.form.get('user_id')
    delete_user(db, user_id)
    
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/get_permissions/<int:user_id>')
def get_permissions(user_id):
    db: Session = next(get_db())
    user_files = get_user_files(db, user_id) or []
    return jsonify(user_files)

@admin_bp.route('/admin/update_permissions', methods=['POST'])
def update_permissions():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    user_id = request.form.get('user_id')
    files = os.listdir("./files")
    selected_files = request.form.getlist('file_access')
    
    for file in files:
        if file in selected_files:
            grant_access(db, user_id, file)
        else:
            revoke_access(db, user_id, file)
    
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/change_password', methods=['POST'])
def change_password():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    update_password(db, user_id, new_password)
    
    return redirect(url_for('admin.admin'))