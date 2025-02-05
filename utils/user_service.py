from sqlalchemy.orm import Session
from utils.models import User
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
    return db.query(User).all()

def delete_user(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

def update_password(db: Session, user_id: int, new_password: str):
    hashed_password = hash_password(new_password)
    db.query(User).filter(User.id == user_id).update({"password": hashed_password})
    db.commit()