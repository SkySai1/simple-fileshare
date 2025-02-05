from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Импортируем модули после создания admin_bp, чтобы избежать циклического импорта
from .admin_main import register_admin_routes
from .admin_users import admin_users_bp
from .admin_permissions import admin_permissions_bp
from .admin_roles import admin_roles_bp
from .admin_api import admin_api_bp

register_admin_routes(admin_bp)
admin_bp.register_blueprint(admin_users_bp)
admin_bp.register_blueprint(admin_permissions_bp)
admin_bp.register_blueprint(admin_roles_bp)
admin_bp.register_blueprint(admin_api_bp)