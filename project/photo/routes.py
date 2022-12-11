from flask import (render_template)
from flask_login import login_required

from . import photo_blueprint
from ..models import File


# Routes
@photo_blueprint.route('/photo-edit')
@login_required
def photo_edit():
    # Uploaded files, with record id DB
    files = File.query.all()
    return_paths = []

    for file in files:
        return_paths.append(file.get_name())

    return render_template('photo.html',
                           files=return_paths)
