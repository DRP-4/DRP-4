import datetime
from app import app
from models import db
from models.task import Task
from models.slot import Slot
from util.response import json_response
from util.user_id import with_user_id
from flask import request, abort
from sqlalchemy import update


@app.route("/api/task/get-all", methods=["GET"])
@with_user_id
def get_tasks(user_id):
    query = db.select(Task).filter(Task.user_id == user_id).order_by(Task.created)
    tasks = db.session.execute(query).scalars().all()
    return json_response(
        [
            {
                "name": t.title,
                "id": t.task_id,
                "description": t.description,
                "complete": t.completed is not None,
                "duration": t.duration_minutes,
            }
            for t in tasks
        ]
    )


@app.route("/api/task/create", methods=["POST"])
@with_user_id
def create_task(user_id):
    body = request.get_json()

    if "name" not in body:
        abort(401)
    name = body["name"]
    if not isinstance(name, str):
        abort(401)

    description = None
    duration = None
    if "description" in body:
        description = body["description"]
        if not isinstance(description, str):
            abort(401)

    if "duration" in body:
        duration = body["duration"]
        if not isinstance(duration, int) or duration < 0:
            abort(401)

    task = Task(
        user_id=user_id, title=name, duration_minutes=duration, description=description
    )
    db.session.add(task)
    db.session.commit()

    return json_response({"id": task.task_id})


@app.route("/api/task/update", methods=["PUT"])
@with_user_id
def update_task(user_id):
    # body has id and possibly new values for all task params
    body = request.get_json()

    if "id" not in body:
        abort(400)
    task_id = body["id"]
    if not isinstance(task_id, int):
        abort(400)

    prop_updates = {}

    if "name" in body:
        name = body["name"]
        if not isinstance(name, str):
            abort(400)
        prop_updates["title"] = name

    if "description" in body:
        description = body["description"]
        if not isinstance(description, str):
            abort(400)
        prop_updates["description"] = description

    if "duration" in body:
        duration = body["duration"]
        if not isinstance(duration, int) or duration < 0:
            abort(400)
        prop_updates["duration_minutes"] = duration

    if "complete" in body:
        complete = body["complete"]
        if not isinstance(complete, bool):
            abort(400)

        prop_updates["complete"] = None
        # find new complete val. If we just completed, its the id of the latest work
        # slot, else it's none/null
        if complete:
            # find the latest work slot
            now = datetime.datetime.now()
            past_slots = (
                db.session.select(Slot)
                .filter(Slot.user_id == user_id, Slot.start <= now, Slot.work)
                .order_by(Slot.start)
            )
            latest_slot = db.session.execute(past_slots).scalars().all()[-1]
            prop_updates["complete"] = latest_slot.slot_id

    if len(prop_updates) > 0:
        # make sure to still verify user id, so users can't modify others tasks
        task = db.session.query(Task).where().one()
        if task is None:
            abort(400)
        # update all changed properties
        stmt = (
            update(Task)
            .where(Task.user_id == user_id, Task.task_id == task_id)
            .values(**prop_updates)
        )
        db.session.execute(stmt)
        db.session.commit()

    return json_response(body)


@app.route("/api/task/delete", methods=["DELETE"])
@with_user_id
def delete_task(user_id):
    # body has task id
    body = request.get_json()

    task = (
        db.session.query(Task)
        .where(Task.user_id == user_id, Task.task_id == body["id"])
        .one()
    )
    if task is None:
        abort(400)

    db.session.delete(task)
    db.session.commit()

    return "", 204
