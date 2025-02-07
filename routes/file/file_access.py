from flask import redirect, url_for, session, request, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import toggle_file_public, get_public_files
from utils.public_links import generate_public_link, delete_public_link

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
    
    @file_bp.route('/generate_public_link/<int:file_id>', methods=['POST'])
    def generate_public_link_route(file_id):
        if "user" not in session:
            return jsonify({"error": "Требуется авторизация"}), 403
        
        username = session["user"]["username"]
        hash_key = generate_public_link(file_id, username)
        return jsonify({"public_link": url_for('file.download_public_file', hash_key=hash_key, _external=True)})

    @file_bp.route('/delete_public_link/<hash_key>', methods=['DELETE'])
    def delete_public_link_route(hash_key):
        if "user" not in session:
            return jsonify({"error": "Требуется авторизация"}), 403
        
        delete_public_link(hash_key)
        return jsonify({"success": True, "message": "Ссылка удалена"})