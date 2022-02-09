#!/usr/bin/python3
"""
returnS the status of the API
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": ["0.0.0.0"]}})


@app.teardown_appcontext
def close_session(self):
    """Closes current context"""
    storage.close()


@app.errorhandler(404)
def error_404(self):
    """Handles 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app_host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    app_port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host=app_host, port=int(app_port), threaded=True)
