import flask
from flask_cors import CORS
from flask_socketio import SocketIO
from importlib import import_module
from os import environ, listdir

from models import db

running_as_dev = "DEV" in environ
static_folder = "../dist"

# Add checks to ensure we've set the right env vars
if "DATABASE_URL" not in environ:
    print("DATABASE_URL environment variable not set!!")
    exit(-1)

# Create flask app instance
app = flask.Flask(__name__, static_folder=static_folder, static_url_path="/")

# Work around deprecated "postgres://" dialect in the
# https://stackoverflow.com/a/66794960
app.config["SQLALCHEMY_DATABASE_URI"] = environ["DATABASE_URL"].replace(
    "postgres://", "postgresql://"
)

# Connect DB plugin to the flask app instance
db.init_app(app)

# This let's all origins access the API, which is probably fine for us.
cors = CORS()
cors.init_app(app)

# Initialize SocketIO
socketio = SocketIO(logger=True)
if running_as_dev:
    socketio.init_app(app, cors_allowed_origins="*")
else:
    socketio.init_app(app)


@socketio.on("connect")
def socketio_connect():
    pass


# Upgrade all HTTP requests to HTTPS
@app.before_request
def upgrade_http():
    r = flask.request
    if (not running_as_dev) and (r.headers["X-Forwarded-Proto"] == "http"):
        url = r.url.replace("http://", "https://", 1)
        return flask.redirect(url, code=301)  # Permenant redirect


@app.after_request
def allow_creds(response):
    if running_as_dev:
        # We shouldn't need this if we are running on the same domain
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


# Load routes
for route in listdir("routes"):
    if route.endswith(".py"):
        import_module(f"routes.{route.removesuffix('.py')}")
