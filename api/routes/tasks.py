import datetime

from app import app
from models import db
from models.task import Task
from models.slot import Slot
from util.response import json_response
from util.user_id import with_user_id
from flask import request, Response
from sqlalchemy.dialects import postgresql


@app.route("/api/task/get-all", methods=["GET"])
@with_user_id
def get_tasks(user_id):
    query = db.select(Task).filter(Task.user_id == user_id).order_by(Task.created)
    tasks = db.session.execute(query).scalars().all()
    return json_response([{"name": t.title, "id": t.id, "description": t.description, "complete": t.complete} for t in tasks])


@app.route("/api/task/update", methods=["POST"])
@with_user_id
def update_task(user_id):
    # body has id and new complete value
    body = request.get_json()

    if "name" in body:
      db.update(Task).where(Task.user_id == user_id and Task.id == body["id"]).values(
              name=body["name"]
      )

    if "description" in body:
      db.update(Task).where(Task.user_id == user_id and Task.id == body["id"]).values(
              name=body["description"]
      )

    if "complete" in body:
      # find new complete val. If we just completed, its the id of the latest work
      # slot, else it's none/null
      new_complete = None
      if body["complete"]:
          # find the latest work slot
          now = datetime.datetime.now()
          past_slots = (
              db.select(Slot)
              .filter(Slot.user_id == user_id and Slot.start <= now and Slot.work)
              .order_by(Slot.start)
          )
          latest_slot = db.session.execute(past_slots).scalars().all()[-1]
          new_complete = latest_slot.slot_id

      # make sure to still verify user id, so users can't modify others tasks
      db.update(Task).where(Task.user_id == user_id and Task.id == body["id"]).values(
          complete=new_complete
      )

    return json_response(body)
