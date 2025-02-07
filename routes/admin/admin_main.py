from flask import render_template, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import get_users
from utils.file_service import get_all_files

def register_admin_routes(admin_bp):
    @admin_bp.route('/')
    def admin():
        db: Session = next(get_db())
        if "user" not in session or not session["user"]["is_admin"]:
            return redirect(url_for('file.index'))
        
        users = get_users(db)
        all_files = get_all_files(db)  # Загружаем файлы из БД
        
        return render_template('admin.html', users=users, files=all_files)