from sqlalchemy.orm import Session
from utils.models import User, FileAccess
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def add_user(db: Session, username: str, password: str, is_admin: bool = False) -> bool:
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password, is_admin=is_admin)
    db.add(user)
    try:
        db.commit()
        return True
    except:
        db.rollback()
        return False

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and check_password(user.password, password):
        return {"id": user.id, "username": user.username, "is_admin": user.is_admin}
    return None

def get_users(db: Session):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username, "is_admin": user.is_admin} for user in users]

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return {"id": user.id, "username": user.username, "is_admin": user.is_admin}
    return None

def delete_user(db: Session, user_id: int):
    # Удаляем все привилегии пользователя
    db.query(FileAccess).filter(FileAccess.user_id == user_id).delete()
    
    # Удаляем пользователя
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

def update_password(db: Session, user_id: int, new_password: str):
    hashed_password = hash_password(new_password)
    db.query(User).filter(User.id == user_id).update({"password": hashed_password})
    db.commit()

def set_admin_status(db: Session, user_id: int, is_admin: bool):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    if not is_admin:
        admin_count = db.query(User).filter(User.is_admin == True).count()
        if admin_count <= 1:
            return False  # Запрет на снятие последнего администратора
    
    user.is_admin = is_admin
    db.commit()
    return True