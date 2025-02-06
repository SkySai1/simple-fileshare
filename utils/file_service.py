import os
from sqlalchemy.orm import Session
from utils.models import FileAccess, File, User
from utils.database import get_db
import datetime

def add_file_to_db(db: Session, user_id: int, filename: str, size: int):
    file_entry = File(filename=filename, owner_id=user_id, size=size, uploaded_at=datetime.datetime.utcnow())
    db.add(file_entry)
    db.commit()
    db.refresh(file_entry)
    return file_entry.id

def register_file_in_db(user_id, filename):
    db = next(get_db())
    file = db.query(File).filter(File.filename == filename, File.owner_id == user_id).first()
    if not file:
        file_id = add_file_to_db(db, user_id, filename, os.path.getsize(f"./files/{filename}"))
    else:
        file_id = file.id
    
    if not db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.file_id == file_id).first():
        db.add(FileAccess(user_id=user_id, file_id=file_id))
        db.commit()

def get_user_files(db: Session, user_id: int):
    file_records = db.query(File).join(FileAccess, File.id == FileAccess.file_id).filter(FileAccess.user_id == user_id).all()
    return [{
        "file_id": file.id,
        "filename": file.filename,
        "size": file.size,
        "modified": file.uploaded_at.strftime("%Y-%m-%d %H:%M"),
        "is_public": file.is_public
    } for file in file_records]

def get_all_files(db: Session):
    file_records = db.query(File).join(User, File.owner_id == User.id).all()
    return [{
        "file_id": file.id,
        "filename": file.filename,
        "size": file.size,
        "modified": file.uploaded_at.strftime("%Y-%m-%d %H:%M"),
        "is_public": file.is_public,
        "owner_username": file.owner.username
    } for file in file_records]

def grant_access(db: Session, user_id: int, file_id: int):
    if not db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.file_id == file_id).first():
        db.add(FileAccess(user_id=user_id, file_id=file_id))
        db.commit()

def revoke_access(db: Session, user_id: int, file_id: int):
    db.query(FileAccess).filter(FileAccess.user_id == user_id, FileAccess.file_id == file_id).delete()
    db.commit()

def set_file_public(db: Session, file_id: int, is_public: bool = True):
    db.query(File).filter(File.id == file_id).update({"is_public": is_public})
    db.commit()

def is_file_public(db: Session, file_id: int) -> bool:
    file = db.query(File).filter(File.id == file_id).first()
    return file is not None and file.is_public

def get_versioned_filename(upload_folder, filename):
    base, ext = os.path.splitext(filename)
    version = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(upload_folder, new_filename)):
        new_filename = f"{base}_v{version}{ext}"
        version += 1
    
    return new_filename

def save_file(file, user_id):
    upload_folder = os.getenv("FILE_FOLDER", "./files")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    versioned_filename = get_versioned_filename(upload_folder, file.filename)
    file_path = os.path.join(upload_folder, versioned_filename)
    file.save(file_path)
    
    db = next(get_db())
    file_id = add_file_to_db(db, user_id, versioned_filename, os.path.getsize(file_path))
    register_file_in_db(user_id, versioned_filename)
    
    return versioned_filename