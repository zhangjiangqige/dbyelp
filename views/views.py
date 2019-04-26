from app import app
from flask import jsonify, request

from db import create_index
from tasks import clean, validate, analyze


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


@app.route('/clean/run', methods=['POST'])
def clean_run():
    task = request.form['task']
    clean.clean(task)
    return jsonify({
        'success': 1
    })


@app.route('/clean/restore', methods=['POST'])
def clean_restore():
    clean.restore()
    return jsonify({
        'success': 1
    })


@app.route('/validate/split', methods=['POST'])
def validate_split():
    validate.split_train_val()
    create_index.create_all()
    return jsonify({
        'success': 1
    })
