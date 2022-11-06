import io
import os

import pytest

from server.app import app


@pytest.fixture
def client():
    return app.test_client()


def test_index(client):
    # Execute
    response = client.get("/", content_type="html/text")

    # Assert
    assert response.status_code == 200


def test_upload_text_stream(client):
    # Setup
    file_name = "text_stream.txt"
    data = {
        'file': (io.BytesIO(b"some text data"), file_name)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Please provide valid image to upload"


def test_upload_textfile(client):
    # Setup
    file = "files/text_file.txt"
    data = {
        'file': (open(file, 'rb'), file)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Please provide valid image to upload"


def test_upload_image_file(client):
    # Setup
    filename = "files/1.png"
    file = open(filename, 'rb')
    data = {
        'file': (file, filename)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 201


def test_upload_image_stream(client):
    # Setup
    image_name = "fake_image_stream.jpg"
    data = {
        'file': (io.BytesIO(b"random_bytes"), image_name)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 201
