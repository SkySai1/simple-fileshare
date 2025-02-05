from flask import Blueprint, render_template, redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import get_users
import os

admin_main_bp = Blueprint('admin_main', __name__)

@admin_main_bp.route('/admin')
def admin():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    users = get_users(db)
    files = os.listdir("./files")
    
    return render_template('admin.html', users=users, files=files)