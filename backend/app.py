import imghdr
import os
import flask
import logging
import flask_cors
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif']

app = flask.Flask(__name__)
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS
cors = flask_cors.CORS(app)


def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != '.jpeg' else '.jpg')


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.error_message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            'message': self.error_message,
            'error': True,
        }


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return error.to_dict(), error.status_code


@app.route("/")
def hello():
    return "Hello, World!"


@app.route('/file/upload', methods=['POST'])
def upload():
    uploaded_file = flask.request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]

        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            raise InvalidUsage("Please provide valid image to upload", status_code=400)

        path = os.path.join(app.config['UPLOAD_PATH'], filename)

        uploaded_file.save(os.path.join(path))

        return {"path": path}, 201
    else:
        raise InvalidUsage("Please provide file to upload", status_code=400)


if __name__ == "__main__":
    app.run(debug=True)
