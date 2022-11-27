from flask import render_template, send_from_directory, current_app

from . import recipes_blueprint


# Routes
@recipes_blueprint.route('/')
def index():
    return render_template('recipes/index.html')


@recipes_blueprint.route('/file/<path:filename>')
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)
