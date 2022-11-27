def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='jgurgul@kupidyn.pl', password='!QAZxsw2'),
                                follow_redirects=True)
    assert response.status_code == 200

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='jgurgul@kupidyn.pl', password='BadPassword'),
                                follow_redirects=True)
    assert response.status_code == 200


def test_login_already_logged_in(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) when the user is already logged in
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='jgurgul@kupidyn.pl', password='BadPassword'),
                                follow_redirects=True)
    assert response.status_code == 200


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/register',
                                data=dict(email='register@kupidyn.pl',
                                          password='kupidyn',
                                          confirm='kupidyn'),
                                follow_redirects=True)
    assert response.status_code == 200

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(email='register2@kupidyn.pl',
                                          password='kupidyn',
                                          confirm='kupidynAle'),  # Does NOT match!
                                follow_redirects=True)
    assert response.status_code == 200


def test_duplicate_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST) using an email address already registered
    THEN check an error message is returned to the user
    """
    test_client.post('/register',
                     data=dict(email='register3@kupidyn.pl',
                               password='kupidyn',
                               confirm='kupidyn'),
                     follow_redirects=True)

    response = test_client.post('/register',
                                data=dict(email='register3@kupidyn.pl',
                                          password='kupidyn',
                                          confirm='kupidyn'),
                                follow_redirects=True)
    assert response.status_code == 200
