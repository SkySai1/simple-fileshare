from flask import Blueprint
from .admin_main import admin_main_bp
from .admin_users import admin_users_bp
from .admin_permissions import admin_permissions_bp
from .admin_roles import admin_roles_bp

admin_bp = Blueprint('admin', __name__)
admin_bp.register_blueprint(admin_main_bp)
admin_bp.register_blueprint(admin_users_bp)
admin_bp.register_blueprint(admin_permissions_bp)
admin_bp.register_blueprint(admin_roles_bp)