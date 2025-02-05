import os
from sqlalchemy.orm import Session
from utils.models import FileAccess
from utils.database import get_db

def grant_access(db: Session, user_id: int, filename: str):
    if not db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.filename == filename).first():
        db.add(FileAccess(user_id=user_id, filename=filename))
        db.commit()

def get_user_files(db: Session, user_id: int):
    return [file.filename for file in db.query(FileAccess).filter(FileAccess.user_id == user_id).all()]

def revoke_access(db: Session, user_id: int, filename: str):
    db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.filename == filename).delete()
    db.commit()

def set_file_public(db: Session, filename: str, is_public: bool = True):
    db.query(FileAccess).filter(FileAccess.filename == filename).update({"is_public": is_public})
    db.commit()

def is_file_public(db: Session, filename: str) -> bool:
    file = db.query(FileAccess).filter(FileAccess.filename == filename).first()
    return file is not None and file.is_public

def save_file(file):
    upload_folder = os.getenv("FILE_FOLDER", "./files")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path

def register_file_in_db(user_id, filename):
    db = next(get_db())
    if not db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.filename == filename).first():
        db.add(FileAccess(user_id=user_id, filename=filename))
        db.commit()