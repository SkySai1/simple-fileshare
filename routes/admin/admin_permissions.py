from flask import Blueprint, request, session, jsonify, redirect, url_for
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import grant_access, revoke_access, get_user_files
import os

admin_permissions_bp = Blueprint('admin_permissions', __name__)

@admin_permissions_bp.route('/get_permissions/<int:user_id>')
def get_permissions(user_id):
    db: Session = next(get_db())
    user_files = get_user_files(db, user_id) or []
    return jsonify(user_files)

@admin_permissions_bp.route('/update_permissions', methods=['POST'])
def update_permissions():
    db: Session = next(get_db())
    if "user" not in session or not session["user"]["is_admin"]:
        return redirect(url_for('file.index'))
    
    user_id = request.form.get('user_id')
    files = os.listdir("./files")
    selected_files = request.form.getlist('file_access')
    
    for file in files:
        if file in selected_files:
            grant_access(db, user_id, file)
        else:
            revoke_access(db, user_id, file)
    
    return redirect(url_for('admin_main.admin'))