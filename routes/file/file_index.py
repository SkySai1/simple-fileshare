from flask import render_template, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import get_user_files

def register_file_index_routes(file_bp):
    @file_bp.route('/')
    def index():
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        user = session["user"]
        files = get_user_files(db, user["id"]) if not user["is_admin"] else get_user_files(db, None)
        public_files = [file for file in files if file["is_public"]]
        
        return render_template('index.html', files=files, public_files=public_files, user=user)