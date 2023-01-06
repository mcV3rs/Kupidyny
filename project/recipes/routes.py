import json
import os

from flask import render_template, send_from_directory, current_app, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import recipes_blueprint
from .. import db
from ..models import File


# Routes
@recipes_blueprint.route('/')
def index():
    return render_template('recipes/index.html')


@recipes_blueprint.route('/file/<path:filename>')
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

        # TODO hardcode wedding_id
        new_file = File(path=filename, wedding_id=1)
        db.session.add(new_file)
        db.session.commit()

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}
