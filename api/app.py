import flask
from flask_cors import CORS
import os

from models import db
from models.task import Task

# Create flask app instance
app = flask.Flask(__name__, static_folder="/www", static_url_path="/")

# Work around deprecated "postgres://" dialect in the 
# https://stackoverflow.com/a/66794960
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace(
    "postgres://", "postgresql://"
)

# Connect DB plugin to the flask app instance
db.init_app(app)

# This let's all origins access the API, which is probably fine for us.
CORS(app)

import routes.index
import routes.tasks
