from flask import Blueprint, render_template, send_from_directory, redirect, url_for, session
import os
from auth import get_user_files

file_bp = Blueprint('file', __name__)
FILES_DIR = "./files"

# Главная страница (отображает файлы)
@file_bp.route('/')
def index():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    user = session["user"]
    if user["is_admin"]:
        files = os.listdir(FILES_DIR)  # Админ видит все файлы
    else:
        files = get_user_files(user["id"])  # Обычный пользователь видит только доступные файлы
    
    return render_template('index.html', files=files, user=user)

# Скачивание файлов с проверкой доступа
@file_bp.route('/download/<path:filename>')
def download_file(filename):
    if "user" not in session:
        return redirect(url_for('auth.login'))

    user = session["user"]
    
    # Проверяем, есть ли у пользователя доступ к файлу
    if user["is_admin"] or filename in get_user_files(user["id"]):
        return send_from_directory(FILES_DIR, filename, as_attachment=True)

    return "Ошибка: У вас нет доступа к этому файлу", 403
