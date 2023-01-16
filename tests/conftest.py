from datetime import datetime

import pytest

from project import create_app, db
from project.models import User, File, Wedding, UserWedding


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

    # Add test pictures
    file1 = File(path='1.png', wedding_id=1, guest_name="Ciocia Ania")
    file2 = File(path='2.jpg', wedding_id=2, guest_name="Asia")
    db.session.add(file1)
    db.session.add(file2)

    # Add test wedding
    wedding1 = Wedding(wife="Justyna", husband="Karol", city="Gliwice", date=datetime(2023, 1, 15))
    wedding2 = Wedding(wife="Karolina", husband="Michał", city="Katowice", date=datetime(2023, 2, 13))
    db.session.add(wedding1)
    db.session.add(wedding2)

    # Add test user wedding connection
    con1 = UserWedding(wedding_id=1, user_id=1)
    con2 = UserWedding(wedding_id=2, user_id=2)
    db.session.add(con1)
    db.session.add(con2)

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


@pytest.fixture(scope='module')
def new_file():
    file = File(path='test_file.png', wedding_id=1, guest_name="Testowy")
    return file
