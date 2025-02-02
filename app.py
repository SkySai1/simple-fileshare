from flask import Flask, render_template, send_from_directory, redirect, url_for, request, session
import os
from auth import authenticate_user, add_user, get_users, grant_access, get_user_files, update_password

app = Flask(__name__)
app.secret_key = "supersecretkey"
FILES_DIR = "./files"

# Главная страница (отображает файлы)
@app.route('/')
def index():
    if "user" not in session:
        return redirect(url_for('login'))
    
    user = session["user"]
    if user["is_admin"]:
        files = os.listdir(FILES_DIR)  # Админ видит все файлы
    else:
        files = get_user_files(user["id"])  # Обычный пользователь видит только доступные файлы
    
    return render_template('index.html', files=files, user=user)

# Функция скачивания файлов с проверкой доступа
@app.route('/download/<path:filename>')
def download_file(filename):
    if "user" not in session:
        return redirect(url_for('login'))

    user = session["user"]
    
    # Проверяем, есть ли у пользователя доступ к файлу
    if user["is_admin"] or filename in get_user_files(user["id"]):
        return send_from_directory(FILES_DIR, filename, as_attachment=True)

    return "Ошибка: У вас нет доступа к этому файлу", 403

# Страница логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = authenticate_user(username, password)

        if user:
            session["user"] = user
            return redirect(url_for('index'))
        return "Ошибка: Неверный логин или пароль", 401
    return render_template('login.html')

# Выход из системы
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

# Админская панель
@app.route('/admin')
def admin():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('index'))
    
    users = get_users()
    files = os.listdir(FILES_DIR)
    return render_template('admin.html', users=users, files=files)

# Добавление пользователя
@app.route('/admin/add_user', methods=['POST'])
def add_user_route():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('index'))

    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == "on"

    if add_user(username, password, is_admin):
        return redirect(url_for('admin'))
    return "Ошибка: Пользователь уже существует", 400

# Выдача доступа к файлам
@app.route('/admin/grant_access', methods=['POST'])
def grant_access_route():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('index'))

    user_id = request.form.get('user_id')
    filename = request.form.get('filename')

    grant_access(user_id, filename)
    return redirect(url_for('admin'))

# Изменение пароля
@app.route('/admin/change_password', methods=['POST'])
def change_password():
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('index'))

    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')

    update_password(user_id, new_password)
    return redirect(url_for('admin'))

if __name__ == "__main__":
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
