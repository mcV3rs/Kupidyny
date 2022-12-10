from flask import (render_template, current_app)
from flask_login import login_required

import project.functions as f
from . import photo_blueprint


# Routes
@photo_blueprint.route('/photo-edit')
@login_required
def photo_edit():
    # Uploaded files
    files = f.list_dir(current_app.config['UPLOAD_PATH'], current_app.config["UPLOAD_EXTENSIONS"])
    current_app.logger.info(files)

    return render_template('photo.html',
                           files=files)
