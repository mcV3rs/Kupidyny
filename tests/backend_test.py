import io
from backend.app import app


def test_index():
    # Setup
    client = app.test_client()

    # Execute
    response = client.get("/",
                          content_type="html/text")

    # Assert
    assert response.status_code == 200
    assert response.data == b"Hello, World!"


def test_upload_text_stream():
    # Setup
    file_name = "text_stream.txt"
    client = app.test_client()
    data = {
        'file': (io.BytesIO(b"some text data"), file_name)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Please provide valid image to upload"


def test_upload_textfile():
    # Setup
    file = "files/text_file.txt"
    client = app.test_client()
    data = {
        'file': (open(file, 'rb'), file)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Please provide valid image to upload"


def test_upload_image_file():
    # Setup
    filename = "files/1.png"
    file = open(filename, 'rb')
    client = app.test_client()
    data = {
        'file': (file, filename)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 201


def test_upload_image_stream():
    # Setup
    image_name = "fake_image_stream.jpg"
    client = app.test_client()
    data = {
        'file': (io.BytesIO(b"random_bytes"), image_name)
    }

    # Execute
    response = client.post('/file/upload', data=data)

    # Assert
    assert response.status_code == 201
    assert response.json['file'] == image_name
