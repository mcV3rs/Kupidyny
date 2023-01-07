import logging
import os
from datetime import datetime
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
    if not inspector.has_table("users") or not inspector.has_table("files"):
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
        # Commit the changes for the users
        db.session.commit()

        echo('Initialized the database!')

    @app.cli.command('populate_db')
    def initialize_database():
        from .models import File
        from .models import User
        from .models import Wedding
        from .models import UserWedding

        """Initialize the database"""
        # Add test admin user
        user1 = User(email='admin@kupidyn.pl', password_plaintext='admin')
        user2 = User(email='wesele1@kupidyn.pl', password_plaintext='wesele1')
        user3 = User(email='wesele2@kupidyn.pl', password_plaintext='wesele2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        # Add test pictures
        file1 = File(path='1.png', wedding_id=1, guest_name="Ciocia Ania")
        file2 = File(path='2.jpg', wedding_id=1, guest_name="Asia")
        file3 = File(path='3.jpg', wedding_id=2, guest_name="Marek")
        file4 = File(path='4.jpg', wedding_id=2, guest_name="Babcia Jadzia")
        db.session.add(file1)
        db.session.add(file2)
        db.session.add(file3)
        db.session.add(file4)

        # Add test wedding
        wedding1 = Wedding(wife="Justyna", husband="Karol", city="Gliwice", date=datetime(2023, 1, 15))
        wedding2 = Wedding(wife="Karolina", husband="Michał", city="Katowice", date=datetime(2023, 2, 13))
        db.session.add(wedding1)
        db.session.add(wedding2)

        # Add test user wedding connection
        con1 = UserWedding(wedding_id=1, user_id=2)
        con2 = UserWedding(wedding_id=2, user_id=3)
        db.session.add(con1)
        db.session.add(con2)

        # Commit the changes for the users
        db.session.commit()

        echo('Populated the database!')

    @app.cli.command('test_db')
    def test_database():
        from .models import File
        from .models import User
        from .models import Wedding
        from .models import UserWedding

        user_wedding = UserWedding.query.filter_by(user_id=2).first()
        print(user_wedding.wedding.get_wife())
