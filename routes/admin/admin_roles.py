from flask import request, session, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import set_admin_status

def register_admin_roles_routes(admin_bp):
    @admin_bp.route('/set_admin_status', methods=['POST'])
    def change_admin_status():
        db: Session = next(get_db())
        if "user" not in session or not session["user"]["is_admin"]:
            return jsonify({"error": "Недостаточно прав"}), 403
        
        user_id = int(request.form.get("user_id"))
        is_admin = request.form.get("is_admin") == "on"
        
        if set_admin_status(db, user_id, is_admin):
            return jsonify({"success": True, "message": "Роль пользователя обновлена"})
        return jsonify({"success": False, "error": "Ошибка при обновлении роли"}), 400