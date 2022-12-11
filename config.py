import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Flask config variables
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='NO_SECRET_KEY')
    UPLOAD_PATH = os.path.join(BASEDIR, 'project/instance')
    UPLOAD_EXTENSIONS = ['.png', '.jpg', '.jpeg']

    # Database config
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'project/instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'project/instance', 'test.db')}")
    WTF_CSRF_ENABLED = False
