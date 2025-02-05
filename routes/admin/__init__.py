from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Импортируем и регистрируем маршруты после создания admin_bp
from .admin_main import register_admin_routes
from .admin_users import register_admin_users_routes
from .admin_permissions import register_admin_permissions_routes
from .admin_roles import register_admin_roles_routes
from .admin_api import register_admin_api_routes

register_admin_routes(admin_bp)
register_admin_users_routes(admin_bp)
register_admin_permissions_routes(admin_bp)
register_admin_roles_routes(admin_bp)
register_admin_api_routes(admin_bp)