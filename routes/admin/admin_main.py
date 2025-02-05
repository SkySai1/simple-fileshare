from flask import render_template, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import get_users
import os

def register_admin_routes(admin_bp):
    @admin_bp.route('/')
    def admin():
        db: Session = next(get_db())
        if "user" not in session or not session["user"]["is_admin"]:
            return redirect(url_for('file.index'))
        
        users = get_users(db)
        files = os.listdir("./files")
        
        return render_template('admin.html', users=users, files=files)