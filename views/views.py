import json
import logging
import pprint

from app import app
from flask import jsonify, request

from db import create_index
from tasks import clean, validate, analyze


logger = logging.getLogger(__name__)


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


@app.route('/analyze/train', methods=['POST'])
def analyze_train():
    params = json.loads(request.form['params'])
    logger.debug('parameters for training: {}'.format(params))
    analyze.train(params)
    return jsonify({
        'success': 1
    })


@app.route('/validate/validate', methods=['POST'])
def validate_validate():
    avg_error = validate.validate_decision_tree()
    if avg_error == None:
        return jsonify({
            'success': 0,
            'msg': 'You must train the model before validating'
        })

    logger.info('average error: {}'.format(avg_error))
    return jsonify({
        'success': 1,
        'average_error': avg_error
    })
