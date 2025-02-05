from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import bcrypt

DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    files = relationship("FileAccess", back_populates="user")

class FileAccess(Base):
    __tablename__ = "file_access"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    is_public = Column(Boolean, default=False)
    user = relationship("User", back_populates="files")

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функции работы с пользователями
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
    db.query(FileAccess).filter(FileAccess.user_id == user_id).delete()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

def update_password(db: Session, user_id: int, new_password: str):
    hashed_password = hash_password(new_password)
    db.query(User).filter(User.id == user_id).update({"password": hashed_password})
    db.commit()

# Функции работы с файлами
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