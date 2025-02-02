from flask import Blueprint, render_template, redirect, url_for, request, session
from auth import authenticate_user

auth_bp = Blueprint('auth', __name__)

# Страница логина
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = authenticate_user(username, password)

        if user:
            session["user"] = user
            return redirect(url_for('file.index'))
        return "Ошибка: Неверный логин или пароль", 401
    return render_template('login.html')

# Выход из системы
@auth_bp.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login'))
