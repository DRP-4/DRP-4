from app import app
from models import db
from models.task import Task
from util.response import json_response
from util.user_id import with_user_id
from flask import request, Response
from sqlalchemy.dialects import postgresql


@app.route("/api/tasks", methods=["GET"])
@with_user_id
def get_tasks(user_id):
    query = db.select(Task).filter(Task.user_id == user_id).order_by(Task.created)
    tasks = db.session.execute(query).scalars().all()
    return json_response([{"name": t.title, "id": t.id} for t in tasks])


@app.route("/api/tasks", methods=["POST"])
@with_user_id
def create_task(user_id):
    body = request.get_json()
    task = Task(title=body["name"], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return Response(status=204)
