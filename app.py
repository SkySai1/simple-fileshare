from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
FILES_DIR = "./files"  # Папка с файлами для скачивания

@app.route('/')
def index():
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    files = os.listdir(FILES_DIR)
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(FILES_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
