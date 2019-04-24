from app import app
from flask import jsonify, request

from tasks import clean


@app.route('/')
def index():
    return jsonify({'success': 1})


@app.route('/clean/tasks')
def clean_tasks():
    return jsonify({
        'success': 1,
        'tasks': [
            {
                'name': k,
                'description': v['description']
            } for k, v in clean.fixes.items()
        ]
    })
