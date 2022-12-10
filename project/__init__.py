import logging
import os
from logging.handlers import RotatingFileHandler

import sqlalchemy as sa
from click import echo
from flask import Flask
from flask.logging import default_handler
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Configuration
db = SQLAlchemy()
login = LoginManager()
login.login_view = "users.login"
BASEDIR = os.path.abspath(os.path.dirname(__file__))


# Application Factory Function
def create_app(config_filename=None):
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_cli_commands(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    return app


# Helper Functions
def initialize_extensions(app):
    db.init_app(app)
    login.init_app(app)

    # Flask-Login configuration
    from project.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    from project.recipes import recipes_blueprint
    from project.users import users_blueprint
    from project.photo import photo_blueprint

    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(photo_blueprint)


def configure_logging(app):
    file_handler = RotatingFileHandler(os.path.join(BASEDIR, 'instance/flask-user-management.log'),
                                       maxBytes=16384,
                                       backupCount=20)
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %('
                                       'filename)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')


def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')
