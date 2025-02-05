from flask import Flask, send_from_directory
import os
from routes.auth_routes import auth_bp
from routes.admin import admin_bp
from routes.file_routes import file_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"
FILES_DIR = os.getenv("FILE_FOLDER", "./files")

# Подключаем маршруты
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(file_bp)

# Маршрут для favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    
    port = int(os.getenv("FLASK_PORT", 5000))  # Порт из переменной окружения, иначе 5000
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]  # True если "true" или "1"
    
    app.run(host='0.0.0.0', port=port, debug=debug)