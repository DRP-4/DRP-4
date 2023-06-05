from app import app, static_folder
import flask


@app.route("/")
def index():
    return flask.send_file(f"{static_folder}/index.html")
