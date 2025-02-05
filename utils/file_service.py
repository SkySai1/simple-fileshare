import os
from sqlalchemy.orm import Session
from utils.models import FileAccess
from utils.database import get_db

def grant_access(db: Session, user_id: int, filename: str):
    if not db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.filename == filename).first():
        db.add(FileAccess(user_id=user_id, filename=filename))
        db.commit()

def get_user_files(db: Session, user_id: int):
    files_info = []
    file_records = db.query(FileAccess).filter(FileAccess.user_id == user_id).all()
    upload_folder = os.getenv("FILE_FOLDER", "./files")
    
    for file_record in file_records:
        file_path = os.path.join(upload_folder, file_record.filename)
        if os.path.exists(file_path):
            file_info = {
                "filename": file_record.filename,
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path)
            }
            files_info.append(file_info)
    
    return files_info

def revoke_access(db: Session, user_id: int, filename: str):
    db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.filename == filename).delete()
    db.commit()

def set_file_public(db: Session, filename: str, is_public: bool = True):
    db.query(FileAccess).filter(FileAccess.filename == filename).update({"is_public": is_public})
    db.commit()

def is_file_public(db: Session, filename: str) -> bool:
    file = db.query(FileAccess).filter(FileAccess.filename == filename).first()
    return file is not None and file.is_public

def get_versioned_filename(upload_folder, filename):
    base, ext = os.path.splitext(filename)
    version = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(upload_folder, new_filename)):
        new_filename = f"{base}_v{version}{ext}"
        version += 1
    
    return new_filename

def save_file(file):
    upload_folder = os.getenv("FILE_FOLDER", "./files")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    versioned_filename = get_versioned_filename(upload_folder, file.filename)
    file_path = os.path.join(upload_folder, versioned_filename)
    file.save(file_path)
    return versioned_filename

def register_file_in_db(user_id, filename):
    db = next(get_db())
    if not db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.filename == filename).first():
        db.add(FileAccess(user_id=user_id, filename=filename))
        db.commit()