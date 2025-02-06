from flask import redirect, url_for, session
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import set_file_public

def register_file_access_routes(file_bp):
    @file_bp.route('/make_public/<filename>', methods=['POST'])
    def make_public(filename):
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        set_file_public(db, filename, is_public=True)
        return redirect(url_for('file.index'))