import redis
import json
import hashlib
from flask import current_app
from datetime import datetime, timedelta
from utils.database import get_db
from utils.models import File

# Инициализация Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_public_link(file_id, username):
    """
    Генерирует хэш-ссылку на файл по file_id и сохраняет её в Redis.
    """
    db = next(get_db())
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise ValueError("Файл не найден")
    
    secret_key = current_app.config['SECRET_KEY']
    timestamp = datetime.now().isoformat(timespec="minutes")
    data = json.dumps({'file': file.stored_filename, 'original_filename': file.original_filename, 'user': username, 'created_at': timestamp})
    hash_key = hashlib.sha256((data + secret_key).encode()).hexdigest()
    redis_client.setex(hash_key, timedelta(hours=24), data)
    return hash_key

def get_public_file(hash_key):
    """
    Проверяет ссылку в Redis и возвращает информацию о файле.
    """
    data = redis_client.get(hash_key)
    if data:
        return json.loads(data)
    return None

def delete_public_link(hash_key):
    """
    Удаляет публичную ссылку из Redis.
    """
    redis_client.delete(hash_key)

def get_all_public_links(username=None, is_admin=False):
    """
    Возвращает все публичные ссылки с расшифровкой данных.
    Если указан username, фильтрует по пользователю.
    """
    all_links = []
    secret_key = current_app.config['SECRET_KEY']
    
    for key in redis_client.scan_iter():
        data = redis_client.get(key)
        if not data:
            continue
        
        try:
            link_info = json.loads(data)
            expected_hash = hashlib.sha256((json.dumps(link_info) + secret_key).encode()).hexdigest()
            if expected_hash == key:  # Проверяем подлинность хэша
                if is_admin or (username and link_info["user"] == username):
                    all_links.append({"hash_key": key, "file": link_info["original_filename"], "user": link_info["user"], "created_at": link_info["created_at"]})
        except (json.JSONDecodeError, KeyError):
            continue  # Игнорируем некорректные данные
    
    return all_links