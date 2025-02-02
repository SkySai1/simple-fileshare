from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from auth import add_user, get_users, grant_access, update_password, delete_user, revoke_access, get_user_files
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

# Получение прав доступа для конкретного пользователя (AJAX)
@admin_bp.route('/admin/get_permissions/<int:user_id>')
def get_permissions(user_id):
    user_files = get_user_files(user_id)

    if user_files is None:
        user_files = []  # Если у пользователя нет файлов, возвращаем пустой список

    return jsonify(user_files)

# Обновление прав доступа к файлам через чекбоксы
@admin_bp.route('/admin/update_permissions', methods=['POST'])
def update_permissions():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    user_id = request.form.get('user_id')
    files = os.listdir("./files")  # Все доступные файлы
    selected_files = request.form.getlist('file_access')  # Файлы, отмеченные чекбоксами

    # Обновляем доступ: сначала удаляем все права, затем выдаем только отмеченные
    for file in files:
        if file in selected_files:
            grant_access(user_id, file)  # Выдаем доступ
        else:
            revoke_access(user_id, file)  # Отзываем доступ

    return redirect(url_for('admin.admin'))


# Изменение пароля пользователя
@admin_bp.route('/admin/change_password', methods=['POST'])
def change_password():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))

    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')

    update_password(user_id, new_password)
    return redirect(url_for('admin.admin'))
