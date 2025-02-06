from flask import redirect, url_for, session, request
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.file_service import set_file_public
from utils.models import File

def register_file_access_routes(file_bp):
    @file_bp.route('/make_public/<int:file_id>', methods=['POST'])
    def make_public(file_id):
        if "user" not in session:
            return redirect(url_for('auth.login'))
        
        db: Session = next(get_db())
        file = db.query(File).filter(File.id == file_id, File.owner_id == session["user"]["id"]).first()
        
        if not file:
            return redirect(url_for('file.index'))
        
        set_file_public(db, file_id, is_public=True)
        return redirect(url_for('file.index'))