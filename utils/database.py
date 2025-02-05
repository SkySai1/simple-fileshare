from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Проверяем существование БД и создаем её при необходимости
if not os.path.exists("users.db"):
    from utils.models import Base, User
    import bcrypt
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin_password = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.add(User(username="admin", password=admin_password, is_admin=True))
    db.commit()
    db.close()