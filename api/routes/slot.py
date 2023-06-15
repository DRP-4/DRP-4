from flask import request
from sqlalchemy import update

from app import app
from models import db
from models.slot import Slot
from models.current_session import CurrentSession
from models.task import Task
from util.response import json_response
from util.user_id import with_user_id
from util.now import instant


@app.route("/api/slot/review", methods=["POST"])
@with_user_id
def review_slot(user_id):
    body = request.get_json()
    if ("slot_id" not in body) or ("feedback" not in body):
        return "Bad Request", 400
    slot_id = body["slot_id"]

    feedback = body["feedback"]
    if feedback < 0 or feedback > 2:
        return "Bad Request", 400

    # check this slot is ours, and that the end has passed
    new_dur = (
        update(Slot)
        .where(Slot.user_id == user_id)
        .where(Slot.slot_id == slot_id)
        .where(Slot.end <= instant())
        .values(feedback=feedback)
    )
    db.session.execute(new_dur)
    db.session.commit()

    return body
