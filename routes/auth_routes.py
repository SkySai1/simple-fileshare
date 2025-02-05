from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    db: Session = next(get_db())
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate_user(db, username, password)
        if user:
            session["user"] = user
            redirect_url = session.pop("redirect_url", url_for('file.index'))
            return jsonify({"success": True, "redirect_url": redirect_url})
        
        return jsonify({"success": False, "error": "Неверный логин или пароль"}), 401
    
    return render_template('login.html')

@auth_bp.before_app_request
def save_redirect():
    if "user" not in session and request.endpoint not in ["auth.login", "static"]:
        session["redirect_url"] = request.url

@auth_bp.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login'))