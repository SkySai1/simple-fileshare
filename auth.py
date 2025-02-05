from sqlalchemy.orm import Session
from utils.database import get_db
from utils.user_service import authenticate_user, add_user, get_users, update_password, delete_user

def login(db: Session, username: str, password: str):
    return authenticate_user(db, username, password)

def register_user(db: Session, username: str, password: str, is_admin: bool = False):
    return add_user(db, username, password, is_admin)

def list_users(db: Session):
    return get_users(db)

def change_password(db: Session, user_id: int, new_password: str):
    return update_password(db, user_id, new_password)

def remove_user(db: Session, user_id: int):
    return delete_user(db, user_id)