from flask import send_from_directory, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import get_user_files, is_file_public
import os

def register_file_download_routes(file_bp):
    @file_bp.route('/download/<path:filename>')
    def download_file(filename):
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        user = session["user"]
        user_files = get_user_files(db, user["id"])
        if user["is_admin"] or any(f["filename"] == filename for f in user_files) or is_file_public(db, filename):
            return send_from_directory("./files", filename, as_attachment=True)
        
        return "Ошибка: У вас нет доступа к этому файлу", 403