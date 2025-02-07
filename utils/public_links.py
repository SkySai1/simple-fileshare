import redis
import json
import hashlib
from flask import current_app
from datetime import timedelta

# Инициализация Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_public_link(stored_filename, username):
    """
    Генерирует хэш-ссылку на файл и сохраняет её в Redis.
    """
    secret_key = current_app.config['SECRET_KEY']
    data = json.dumps({'file': stored_filename, 'user': username})
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