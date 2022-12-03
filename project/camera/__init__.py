from flask import Blueprint

camera_blueprint = Blueprint('camera',
                             __name__,
                             template_folder='templates')

from . import routes
