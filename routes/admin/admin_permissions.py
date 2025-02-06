from flask import request, session, jsonify, redirect, url_for
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import grant_access, revoke_access, get_user_files, get_all_files

def register_admin_permissions_routes(admin_bp):
    @admin_bp.route('/get_permissions_filenames/<int:user_id>')
    def get_permissions_filenames(user_id):
        db: Session = next(get_db())
        user_files = get_user_files(db, user_id) or []
        return jsonify([{"file_id": f["file_id"], "filename": f["filename"]} for f in user_files])

    @admin_bp.route('/update_permissions', methods=['POST'])
    def update_permissions():
        db: Session = next(get_db())
        if "user" not in session or not session["user"]["is_admin"]:
            return redirect(url_for('file.index'))
        
        user_id = request.form.get('user_id')
        all_files = get_all_files(db)  # Получаем файлы из БД
        selected_files = request.form.getlist('file_access')
        
        for file in all_files:
            if str(file["file_id"]) in selected_files:
                grant_access(db, user_id, file["file_id"])
            else:
                revoke_access(db, user_id, file["file_id"])
        
        return redirect(url_for('admin.admin'))