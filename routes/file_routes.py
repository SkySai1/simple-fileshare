from flask import Blueprint, render_template, send_from_directory, redirect, url_for, session, request, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import get_user_files, grant_access, revoke_access, set_file_public, is_file_public, save_file, register_file_in_db
import os

file_bp = Blueprint('file', __name__)
FILES_DIR = "./files"

@file_bp.route('/')
def index():
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    db: Session = next(get_db())
    user = session["user"]
    files = get_user_files(db, user["id"]) if not user["is_admin"] else [
        {"filename": f, "size": os.path.getsize(os.path.join(FILES_DIR, f)), "modified": os.path.getmtime(os.path.join(FILES_DIR, f))}
        for f in os.listdir(FILES_DIR)
    ]
    public_files = [f for f in os.listdir(FILES_DIR) if is_file_public(db, f)]
    
    return render_template('index.html', files=files, public_files=public_files, user=user)

@file_bp.route('/download/<path:filename>')
def download_file(filename):
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    db: Session = next(get_db())
    user = session["user"]
    user_files = get_user_files(db, user["id"])
    if user["is_admin"] or any(f["filename"] == filename for f in user_files) or is_file_public(db, filename):
        return send_from_directory(FILES_DIR, filename, as_attachment=True)
    
    return "Ошибка: У вас нет доступа к этому файлу", 403

@file_bp.route('/make_public/<filename>', methods=['POST'])
def make_public(filename):
    if "user" not in session:
        return redirect(url_for('auth.login'))
    
    db: Session = next(get_db())
    set_file_public(db, filename, is_public=True)
    return redirect(url_for('file.index'))

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    if "user" not in session:
        return jsonify({"error": "Требуется авторизация"}), 403
    
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден в запросе"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Пустое имя файла"}), 400
    
    versioned_filename = save_file(file)
    register_file_in_db(session["user"]["id"], versioned_filename)
    
    return jsonify({"success": True, "message": "Файл загружен", "file": versioned_filename})