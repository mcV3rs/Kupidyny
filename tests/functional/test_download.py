from project import create_app
from project.models import Wedding


def test_wedding_book_invalid_uuid_with_fixture():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/book/<uuid>' page is requested (GET)
    THEN check that the response is 302
    """
    flask_app = create_app('flask_test.cfg')

    with flask_app.test_client() as test_client:
        wedding_book = test_client.get('/wedding-book/6305bcba-39dc-492c-bd3f-fdf9e1397964')

        assert wedding_book.status_code == 302


def test_download_html_invalid_uuid_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/book/<uuid>' page is requested (GET)
    THEN check that the response is 302
    """
    response = test_client.get('/wedding-book/6305bcba-39dc-492c-bd3f-fdf9e1397964')

    assert response.status_code == 302


def test_wedding_book_valid_uuid_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/book/<uuid>' page is requested (GET)
    THEN check that the response is 200
    """

    uuid = Wedding.query.filter_by(id=1).first().get_uuid()
    response = test_client.get(f'/wedding-book/{uuid}')

    assert response.status_code == 200


def test_wedding_download_html_valid_id_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/download/html/1' page is requested (GET)
    THEN check that the response is 200
    """

    wedding = Wedding.query.filter_by(id=1).first()
    response = test_client.get(f'/download/html/1')

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'attachment; filename={wedding.get_wife()}_{wedding.get_husband()}_fotobook.html'


def test_wedding_download_pdf_valid_id_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/download/pdf/1' page is requested (GET)
    THEN check that the response is 200
    """

    wedding = Wedding.query.filter_by(id=1).first()
    response = test_client.get(f'/download/pdf/1')

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'attachment; filename={wedding.get_wife()}_{wedding.get_husband()}_fotobook.pdf'


def test_wedding_download_cupid_valid_id_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/download/cupid/1' page is requested (GET)
    THEN check that the response is 200
    """

    wedding = Wedding.query.filter_by(id=1).first()
    response = test_client.get(f'/download/cupid/1')

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'attachment; filename={wedding.get_wife()}_{wedding.get_husband()}_fotobook.cupid'


def test_wedding_download_zip_valid_id_with_fixture(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing with login user
    WHEN the '/download/zip/1' page is requested (GET)
    THEN check that the response is 200
    """

    wedding = Wedding.query.filter_by(id=1).first()
    response = test_client.get(f'/download/zip/1')

    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'attachment; filename={wedding.get_wife()}_{wedding.get_husband()}_fotobook.zip'
