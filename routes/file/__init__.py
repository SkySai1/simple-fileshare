from flask import Blueprint

file_bp = Blueprint('file', __name__, url_prefix='/file')

from .file_index import register_file_index_routes
from .file_download import register_file_download_routes
from .file_upload import register_file_upload_routes
from .file_access import register_file_access_routes

register_file_index_routes(file_bp)
register_file_download_routes(file_bp)
register_file_upload_routes(file_bp)
register_file_access_routes(file_bp)