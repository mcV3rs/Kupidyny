import imghdr
import os
import flask
import flask_cors
from werkzeug.utils import secure_filename
import project.functions as f

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']
TEMPLATE_FOLDER = os.path.abspath('../client')

app = flask.Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.config["UPLOAD_PATH"] = UPLOAD_FOLDER
app.config["UPLOAD_EXTENSIONS"] = ALLOWED_EXTENSIONS
cors = flask_cors.CORS(app)


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
def index():
    files = f.list_dir(app.config['UPLOAD_PATH'], app.config["UPLOAD_EXTENSIONS"])

    return flask.render_template('upload.html', files=files)


@app.route('/file/upload', methods=['POST'])
def upload_files():
    uploaded_file = flask.request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = (os.path.splitext(filename)[1]).lower()

        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            raise InvalidUsage("Please provide valid image to upload", status_code=400)

        path = os.path.join(app.config['UPLOAD_PATH'], filename)

        uploaded_file.save(path)

        return {"path": path}, 201
    else:
        raise InvalidUsage("Please provide file to upload", status_code=400)


@app.route('/file/<filename>')
def show_files(filename):
    return flask.send_from_directory(app.config['UPLOAD_PATH'], filename)


if __name__ == "__main__":
    app.run(debug=True)
