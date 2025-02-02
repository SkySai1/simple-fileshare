from flask import Blueprint, render_template, redirect, url_for, request, session
from auth import add_user, get_users, grant_access, update_password, delete_user, revoke_access
import os

admin_bp = Blueprint('admin', __name__)

# Админская панель
@admin_bp.route('/admin')
def admin():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    users = get_users()
    files = os.listdir("./files")
    return render_template('admin.html', users=users, files=files)

# Добавление пользователя
@admin_bp.route('/admin/add_user', methods=['POST'])
def add_user_route():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == "on"

    if add_user(username, password, is_admin):
        return redirect(url_for('admin.admin'))
    return "Ошибка: Пользователь уже существует", 400

# Удаление пользователя
@admin_bp.route('/admin/remove_user', methods=['POST'])
def remove_user():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    user_id = request.form.get('user_id')
    delete_user(user_id)

    return redirect(url_for('admin.admin'))

# Выдача доступа к файлам
@admin_bp.route('/admin/grant_access', methods=['POST'])
def grant_access_route():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    user_id = request.form.get('user_id')
    filename = request.form.get('filename')

    grant_access(user_id, filename)
    return redirect(url_for('admin.admin'))

# Отзыв доступа к файлу
@admin_bp.route('/admin/revoke_access', methods=['POST'])
def revoke_file_access():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    user_id = request.form.get('user_id')
    filename = request.form.get('filename')

    revoke_access(user_id, filename)
    return redirect(url_for('admin.admin'))

# Изменение пароля
@admin_bp.route('/admin/change_password', methods=['POST'])
def change_password():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')

    update_password(user_id, new_password)
    return redirect(url_for('admin.admin'))
