from flask import jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import get_users, get_user_by_id

def register_admin_api_routes(admin_bp):
    @admin_bp.route('/users', methods=['GET'])
    def get_users_list():
        db: Session = next(get_db())
        users = get_users(db)
        return jsonify(users)

    @admin_bp.route('/user/<int:user_id>', methods=['GET'])
    def get_user_info(user_id):
        db: Session = next(get_db())
        user = get_user_by_id(db, user_id)
        if user:
            return jsonify(user)
        return jsonify({"error": "Пользователь не найден"}), 404