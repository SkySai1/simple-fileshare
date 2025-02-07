from flask import render_template, redirect, url_for, session, jsonify, request
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import get_user_files, get_all_files, get_public_files, delete_file

def register_file_index_routes(file_bp):
    @file_bp.route('/')
    def index():
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        user = session["user"]
        
        files = get_user_files(db, user["id"])  # Всегда получаем файлы пользователя
        all_files = get_all_files(db) if user["is_admin"] else []  # Админ может видеть все файлы
        
        public_files = [file for file in files if file["is_public"]]
        
        return render_template('index.html', files=files, public_files=public_files, all_files=all_files, user=user)

    @file_bp.route('/get_user_files')
    def get_user_files_api():
        if "user" not in session:
            return jsonify({"error": "Требуется авторизация"}), 403
        
        db: Session = next(get_db())
        user = session["user"]
        
        if request.args.get("public") == "true":
            return jsonify(get_public_files(db))
        
        if request.args.get("admin") == "true":
            if not user["is_admin"]:
                return jsonify({"error": "Недостаточно прав"}), 403
            return jsonify(get_all_files(db))
        
        return jsonify(get_user_files(db, user["id"]))