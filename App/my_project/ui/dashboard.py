import os
import threading
from flask import Blueprint, send_file, Response, jsonify

ui_bp = Blueprint('ui_bp', __name__)

@ui_bp.route('/', methods=['GET'])
def index():
    html_path = os.path.join(os.path.dirname(__file__), 'dashboard.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, mimetype='text/html')
    return "<h1>Frontend template not found.</h1>", 404

@ui_bp.route('/api/shutdown', methods=['POST'])
def shutdown():
    def stop_server():
        import time
        time.sleep(0.5)
        os._exit(0)

    threading.Thread(target=stop_server, daemon=True).start()
    return jsonify({"message": "Сервер зупиняється..."}), 200
