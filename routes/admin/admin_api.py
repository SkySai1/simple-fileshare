from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import get_users, get_user_by_id

admin_api_bp = Blueprint('admin_api', __name__)

@admin_api_bp.route('/admin/users', methods=['GET'])
def get_users_list():
    db: Session = next(get_db())
    users = get_users(db)
    return jsonify(users)

@admin_api_bp.route('/admin/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    db: Session = next(get_db())
    user = get_user_by_id(db, user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "Пользователь не найден"}), 404