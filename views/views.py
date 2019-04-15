from app import app
from flask import jsonify, request


@app.route('/')
def index():
    return jsonify({'success': 1})
