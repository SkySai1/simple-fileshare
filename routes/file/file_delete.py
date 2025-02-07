from flask import session, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import delete_file

def register_file_delete_routes(file_bp):
    @file_bp.route('/delete/<int:file_id>', methods=['DELETE'])
    def delete_file_api(file_id):
        if "user" not in session:
            return jsonify({"error": "Требуется авторизация"}), 403
        
        db: Session = next(get_db())
        user_id = session["user"]["id"]
        
        try:
            delete_file(db, user_id, file_id)
            return jsonify({"success": True})
        except PermissionError:
            return jsonify({"error": "У вас нет прав на удаление этого файла"}), 403
        except ValueError:
            return jsonify({"error": "Файл не найден"}), 404