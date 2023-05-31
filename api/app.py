import pprint
import flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

db = SQLAlchemy()
app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Task(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.func.now())


def json_response(payload, status=200):
    r = flask.Response(flask.json.dumps(payload))
    r.headers["Content-Type"] = "application/json"
    r.status_code = status
    # Security, who cares!
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/tasks")
def tasks():
    tasks = db.session.execute(db.select(Task).order_by(Task.created)).scalars().all()
    return json_response([{"name": t.title, "id": t.id} for t in tasks])

chats = []

