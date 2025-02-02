import sqlite3
import bcrypt

DB_PATH = "users.db"

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        is_admin BOOLEAN NOT NULL DEFAULT 0)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS file_access (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        filename TEXT NOT NULL,
                        UNIQUE(user_id, filename),  -- Уникальный индекс для предотвращения дублирования
                        FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()

# Хеширование пароля
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Проверка пароля
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Проверка логина пользователя
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password, is_admin FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password(user[1], password):
        return {"id": user[0], "username": username, "is_admin": bool(user[2])}
    return None

# Добавление нового пользователя
def add_user(username, password, is_admin=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
                       (username, hashed_password, is_admin))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Пользователь уже существует

# Обновление пароля пользователя
def update_password(user_id, new_password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
    conn.commit()
    conn.close()

# Получение списка пользователей
def get_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, is_admin FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Назначение доступа к файлу
def grant_access(user_id, filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Проверяем, есть ли уже доступ к файлу у пользователя
    cursor.execute("SELECT COUNT(*) FROM file_access WHERE user_id = ? AND filename = ?", (user_id, filename))
    if cursor.fetchone()[0] == 0:  # Если доступ отсутствует, добавляем
        cursor.execute("INSERT INTO file_access (user_id, filename) VALUES (?, ?)", (user_id, filename))
        conn.commit()

    conn.close()

# Получение списка файлов, доступных пользователю
def get_user_files(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM file_access WHERE user_id = ?", (user_id,))
    files = [row[0] for row in cursor.fetchall()]
    conn.close()
    return files

# Функция удаления пользователя
def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Удаляем все записи о доступе пользователя к файлам
    cursor.execute("DELETE FROM file_access WHERE user_id = ?", (user_id,))
    # Удаляем пользователя
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    
    conn.commit()
    conn.close()

# Функция отзыва доступа к файлу
def revoke_access(user_id, filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM file_access WHERE user_id = ? AND filename = ?", (user_id, filename))
    conn.commit()
    conn.close()

# Запускаем инициализацию БД при импорте
init_db()


