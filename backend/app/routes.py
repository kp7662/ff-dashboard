from flask import jsonify
from app import app

@app.route('/api/data')
def get_data():
    data = {
        "items": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200},
            {"id": 3, "name": "Item 3", "value": 300},
        ]
    }
    return jsonify(data)

# @app.route('/')
# def home():
#     return "Welcome to the Flask backend!"

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')