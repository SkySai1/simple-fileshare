from flask import Blueprint, render_template, send_from_directory, redirect, url_for, session, request
from sqlalchemy.orm import Session
from utils.db_utils import get_db, get_user_files, grant_access, revoke_access, set_file_public, is_file_public
import os

file_bp = Blueprint('file', __name__)
FILES_DIR = "./files"

@file_bp.route('/')
def index():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    db: Session = next(get_db())
    user = session["user"]
    files = get_user_files(db, user["id"]) if not user["is_admin"] else os.listdir(FILES_DIR)
    public_files = [f for f in os.listdir(FILES_DIR) if is_file_public(db, f)]
    
    return render_template('index.html', files=files, public_files=public_files, user=user)

@file_bp.route('/download/<path:filename>')
def download_file(filename):
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    db: Session = next(get_db())
    user = session["user"]
    if user["is_admin"] or filename in get_user_files(db, user["id"]) or is_file_public(db, filename):
        return send_from_directory(FILES_DIR, filename, as_attachment=True)
    
    return "Ошибка: У вас нет доступа к этому файлу", 403

@file_bp.route('/make_public/<filename>', methods=['POST'])
def make_public(filename):
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    db: Session = next(get_db())
    set_file_public(db, filename, is_public=True)
    return redirect(url_for('file.index'))