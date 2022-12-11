import json
import os

from flask import render_template, send_from_directory, current_app, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import recipes_blueprint


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.error_message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            'message': self.error_message,
            'error': True,
        }


# Routes
@recipes_blueprint.route('/')
def index():
    return render_template('recipes/index.html')


@recipes_blueprint.route('/file/<path:filename>')
@login_required
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@recipes_blueprint.route('/file/upload', methods=['POST'])
@login_required
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    if filename != '':
        file_ext = (os.path.splitext(filename)[1]).lower()

        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

        path = os.path.join(current_app.config['UPLOAD_PATH'], filename)

        uploaded_file.save(path)

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}
