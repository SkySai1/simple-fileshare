from flask import send_from_directory, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import get_user_files, is_file_public
from utils.models import File
import os

def register_file_download_routes(file_bp):
    @file_bp.route('/download/<int:file_id>')
    def download_file(file_id):
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        user = session["user"]
        file = db.query(File).filter(File.id == file_id).first()
        
        if not file:
            return "Ошибка: Файл не найден", 404
        
        user_files = get_user_files(db, user["id"])
        if user["is_admin"] or any(f["file_id"] == file.id for f in user_files) or is_file_public(db, file_id):
            return send_from_directory("./files", file.stored_filename, as_attachment=True, download_name=file.original_filename)
        
        return "Ошибка: У вас нет доступа к этому файлу", 403