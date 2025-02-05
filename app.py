from flask import Flask
from routes.admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)