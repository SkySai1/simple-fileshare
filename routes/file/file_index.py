from flask import render_template, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import get_user_files, is_file_public
import os
import datetime

def register_file_index_routes(file_bp):
    @file_bp.route('/')
    def index():
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        user = session["user"]
        files = get_user_files(db, user["id"]) if not user["is_admin"] else [
            {
                "filename": f,
                "size": os.path.getsize(os.path.join("./files", f)),
                "modified": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join("./files", f))).strftime('%Y-%m-%d %H:%M:%S')
            }
            for f in os.listdir("./files")
        ]
        public_files = [
            {
                "filename": f,
                "size": os.path.getsize(os.path.join("./files", f)),
                "modified": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join("./files", f))).strftime('%Y-%m-%d %H:%M:%S')
            }
            for f in os.listdir("./files") if is_file_public(db, f)
        ]
        
        return render_template('index.html', files=files, public_files=public_files, user=user)