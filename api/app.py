from http.client import NO_CONTENT
import pprint
import flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_cors import CORS


db = SQLAlchemy()
app = flask.Flask(__name__, static_folder="/www", static_url_path="/")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
# This let's all origins access the API, which is probably fine for us.
CORS(app)


class Task(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    created = sa.Column(sa.DateTime, server_default=sa.func.now())


def json_response(payload, status=200):
    r = flask.Response(flask.json.dumps(payload))
    r.headers["Content-Type"] = "application/json"
    r.status_code = status
    return r


@app.route("/")
def index():
    return flask.send_file("/www/index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = db.session.execute(db.select(Task).order_by(Task.created)).scalars().all()
    return json_response([{"name": t.title, "id": t.id} for t in tasks])

    # tasks = [{"name": "Task 1", "id": 1}, {"name": "Task 2", "id": 2}]
    # return json_response(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    body = flask.request.get_json()
    task = Task(title=body["name"])
    db.session.add(task)
    db.session.commit()

    return ("", NO_CONTENT)


chats = []
