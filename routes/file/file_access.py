from flask import redirect, url_for, session, request, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import toggle_file_public, get_public_files

def register_file_access_routes(file_bp):
    @file_bp.route('/toggle_public/<int:file_id>', methods=['POST'])
    def toggle_public(file_id):
        if "user" not in session:
            return jsonify({"error": "Требуется авторизация"}), 403
        
        db: Session = next(get_db())
        user_id = session["user"]["id"]
        
        try:
            new_status = toggle_file_public(db, user_id, file_id)
            return jsonify({"success": True, "is_public": new_status})
        except PermissionError:
            return jsonify({"error": "У вас нет прав на изменение доступа к файлу"}), 403
        except ValueError:
            return jsonify({"error": "Файл не найден"}), 404

    @file_bp.route('/public_files')
    def public_files():
        db: Session = next(get_db())
        files = get_public_files(db)
        return jsonify(files)