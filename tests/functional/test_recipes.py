from project import create_app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200


def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_login_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200


def test_login_page_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 302


def test_register_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/login')
        assert response.status_code == 200


def test_register_page_with_user(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 302


def test_profile_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/profile')
        assert response.status_code == 302


def test_profile_page_with_user(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/profile' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/profile')
    assert response.status_code == 200


def test_qr_hub_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/qr' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/qr')
        assert response.status_code == 302


def test_qr_hub_with_user(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/qr' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/qr')
    assert response.status_code == 200


def test_book_edit_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/book-edit' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app('flask_test.cfg')

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/book-edit')
        assert response.status_code == 302


def test_book_edit_with_user(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/qr' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/book-edit')
    assert response.status_code == 200
