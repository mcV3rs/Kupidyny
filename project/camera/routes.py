from flask import render_template
from flask_login import login_required

from . import camera_blueprint


# Routes
@camera_blueprint.route('/camera')
@login_required
def camera():
    return render_template('camera.html')
