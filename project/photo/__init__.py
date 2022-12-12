from flask import Blueprint

photo_blueprint = Blueprint('photo',
                            __name__,
                            template_folder='templates')

from . import routes
