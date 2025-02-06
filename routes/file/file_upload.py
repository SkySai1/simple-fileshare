from flask import request, session, jsonify
from utils.file_service import save_file, register_file_in_db

def register_file_upload_routes(file_bp):
    @file_bp.route('/upload', methods=['POST'])
    def upload_file():
        if "user" not in session:
            return jsonify({"error": "Требуется авторизация"}), 403
        
        if 'file' not in request.files:
            return jsonify({"error": "Файл не найден в запросе"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Пустое имя файла"}), 400
        
        versioned_filename = save_file(file)
        register_file_in_db(session["user"]["id"], versioned_filename)
        
        return jsonify({"success": True, "message": "Файл загружен", "file": versioned_filename})