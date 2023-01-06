import io
import os

from config import BASEDIR
from project import create_app


def test_download_file():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/file/1.png' page is requested (GET)
    THEN check that the response is 302 (redirect)
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/file/1.png')
        assert response.status_code == 200


def test_download_file_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/file/1.png' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/file/1.png')

    assert response.status_code == 200


def test_upload_file():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/file/upload' page is requested (GET)
    THEN check that the response is 302 (redirect)
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/file/upload')
        assert response.status_code == 404


def test_upload_file_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/file/upload' page is requested (POST)
    THEN check that the response is 302 (redirect)
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/file/upload')
        assert response.status_code == 302


def test_upload_file_with_fixture_text_stream(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/file/upload' page is requested (POST)
    THEN check that the response is 400 (BAD REQUEST)
    """
    file_name = "text_stream.txt"
    data = {
        'file': (io.BytesIO(b"some text data"), file_name)
    }

    response = test_client.post('/file/upload', data=data)

    assert response.status_code == 400


def test_upload_file_with_fixture_text_file(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/file/upload' page is requested (POST)
    THEN check that the response is 400 (BAD REQUEST)
    """
    file = os.path.join(BASEDIR, 'tests/files', 'text_file.txt')
    data = {
        'file': (open(file, 'rb'), file)
    }

    response = test_client.post('/file/upload', data=data)

    assert response.status_code == 400


def test_upload_file_with_fixture_image_file(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/file/upload' page is requested (POST)
    THEN check that the response is 201 (CREATED)
    """
    file = os.path.join(BASEDIR, 'tests/files', '1.jpg')
    data = {
        'file': (open(file, 'rb'), file)
    }

    response = test_client.post('/file/upload', data=data)

    assert response.status_code == 201


def test_upload_file_with_fixture_image_stream(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/file/upload' page is requested (POST)
    THEN check that the response is 201 (CREATED)
    """
    file = "fake_image_stream.jpg"
    data = {
        'file': (io.BytesIO(b"random_bytes"), file)
    }

    response = test_client.post('/file/upload', data=data)

    assert response.status_code == 201
