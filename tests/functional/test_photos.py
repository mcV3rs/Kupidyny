import io
import os

from config import BASEDIR
from project import create_app
from project.models import Wedding


def test_download_file():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/static/img/favicon.png' page is requested (GET)
    THEN check that the response is 200
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/static/img/favicon.png')
        assert response.status_code == 200


def test_download_file_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/static/img/favicon.png' page is requested (GET)
    THEN check that the response is 200
    """
    response = test_client.get('/static/img/favicon.png')

    assert response.status_code == 200


def test_upload_file():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/edit-picture/niepoprawny-link' page is requested (GET)
    THEN check that the response is 404
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/edit-picture/niepoprawny-link')
        assert response.status_code == 404


def test_upload_file_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/edit-picture/niepoprawny-link' page is requested (POST)
    THEN check that the response is 404
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/edit-picture/niepoprawny-link')
        assert response.status_code == 404


def test_upload_file_with_fixture_text_stream(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/edit-picture/<uuid>' page is requested (POST)
    THEN check that the response is 302
    """
    file_name = "text_stream.txt"
    data = {
        'file': (io.BytesIO(b"some text data"), file_name)
    }

    uuid = Wedding.query.filter_by(id=1).first().get_uuid()
    response = test_client.post(f'/edit-picture/{uuid}', data=data)

    assert response.status_code == 302


def test_upload_file_with_fixture_text_file(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/edit-picture/<uuid>' page is requested (POST)
    THEN check that the response is 302
    """
    file = os.path.join(BASEDIR, 'tests/files', 'text_file.txt')
    data = {
        'file': (open(file, 'rb'), file)
    }

    uuid = Wedding.query.filter_by(id=1).first().get_uuid()
    response = test_client.post(f'/edit-picture/{uuid}', data=data)

    assert response.status_code == 302


def test_upload_file_with_fixture_image_file(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/edit-picture/<uuid>' page is requested (POST)
    THEN check that the response is 200
    """
    file = os.path.join(BASEDIR, 'tests/files', '1.jpg')
    data = {
        'file': (open(file, 'rb'), file)
    }

    uuid = Wedding.query.filter_by(id=1).first().get_uuid()
    response = test_client.post(f'/edit-picture/{uuid}', data=data)

    assert response.status_code == 200


def test_upload_file_with_fixture_image_stream(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/edit-picture/<uuid>' page is requested (POST)
    THEN check that the response is 200
    """
    file = "fake_image_stream.jpg"
    data = {
        'file': (io.BytesIO(b"random_bytes"), file)
    }

    uuid = Wedding.query.filter_by(id=1).first().get_uuid()
    response = test_client.post(f'/edit-picture/{uuid}', data=data)

    assert response.status_code == 200
