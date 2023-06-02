from app import app
from models import db
from models.task import Task
from util.response import json_response
from http.client import NO_CONTENT
import flask

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = db.session.execute(db.select(Task).order_by(Task.created)).scalars().all()
    return json_response([{"name": t.title, "id": t.id} for t in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    body = flask.request.get_json()
    task = Task(title=body["name"])
    db.session.add(task)
    db.session.commit()

    return ("", NO_CONTENT)
