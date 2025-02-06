from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from utils.database import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    files = relationship("File", back_populates="owner", cascade="all, delete-orphan")
    access = relationship("FileAccess", back_populates="user", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)  # Оригинальное имя файла
    stored_filename = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # UUID-имя
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    size = Column(Integer, nullable=False)
    is_public = Column(Boolean, default=False)
    owner = relationship("User", back_populates="files")
    access = relationship("FileAccess", back_populates="file", cascade="all, delete-orphan")

class FileAccess(Base):
    __tablename__ = "file_access"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="access")
    file = relationship("File", back_populates="access")