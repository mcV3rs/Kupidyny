import flask
import flask_cors

app = flask.Flask(__name__)

cors = flask_cors.CORS(app)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
