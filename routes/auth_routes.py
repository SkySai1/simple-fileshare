from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from auth import authenticate_user

auth_bp = Blueprint('auth', __name__)

# Страница логина
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = authenticate_user(username, password)

        if user:
            session["user"] = user
            redirect_url = session.pop("redirect_url", url_for('file.index'))  # Перенаправляем на сохранённую страницу или на главную
            return jsonify({"success": True, "redirect_url": redirect_url})

        return jsonify({"success": False, "error": "Неверный логин или пароль"}), 401

    # Если GET-запрос, отображаем форму
    return render_template('login.html')

# Middleware для сохранения редиректа перед авторизацией
@auth_bp.before_app_request
def save_redirect():
    if "user" not in session and request.endpoint not in ["auth.login", "static"]:
        session["redirect_url"] = request.url

# Выход из системы
@auth_bp.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login'))
