import pytest

from project import create_app, db
from project.models import User


# Fixtures
@pytest.fixture(scope='module')
def new_user():
    user = User('jgurgul@kupidyn.pl', '!QAZxsw2')
    return user


@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='jgurgul@kupidyn.pl', password_plaintext='!QAZxsw2')
    user2 = User(email='testowy@kupidyn.pl', password_plaintext='Password')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='jgurgul@kupidyn.pl', password='!QAZxsw2'),
                     follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='module')
def cli_test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    runner = flask_app.test_cli_runner()

    yield runner
