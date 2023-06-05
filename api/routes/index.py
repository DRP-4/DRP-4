from app import app
import flask


@app.route("/")
def index():
    return flask.send_file("/www/index.html")
