from flask import request
from sqlalchemy import update

from app import app
from models import db
from models.slot import Slot
from models.current_session import CurrentSession
from models.task import Task
from util.response import json_response
from util.user_space_id import with_space_id
from util.now import instant

import datetime
import util.times as times


@app.route("/api/slot/review", methods=["POST"])
@with_space_id
def review_slot(space_id):
    body = request.get_json()
    if ("slot_id" not in body) or ("feedback" not in body):
        return "Bad Request", 400
    slot_id = body["slot_id"]
    if not isinstance(slot_id, int):
        return "Bad Request", 400
    feedback = body["feedback"]
    if not isinstance(feedback, int) or feedback not in [1, 2, 3]:
        return "Bad Request", 400

    # Get the slot
    slot = (
        db.session.execute(
            db.select(Slot).where(
                Slot.slot_id == slot_id, Slot.space_id == space_id, Slot.work == True
            )
        )
        .scalars()
        .one_or_none()
    )
    if slot is None:
        return "File Not Found", 404

    # Update the reaction
    db.session.execute(
        update(Slot)
        .where(Slot.slot_id == slot_id, Slot.space_id == space_id)
        .values(feedback=feedback)
    )

    # Get the break slot after
    next_break_slot = (
        db.session.execute(
            db.select(Slot).where(
                Slot.start == slot.end,
                Slot.space_id == space_id,
                Slot.work.is_(False),
                Slot.end >= instant()
            )
        )
        .scalars()
        .one_or_none()
    )
    if next_break_slot is None:
        # Allow reviews for work slots even if they are the last thing that happens
        # Just don't do any rescheduling in this case
        db.session.commit()
        return "", 204

    # Get the work slot after
    next_work_slot = (
        db.session.execute(
            db.select(Slot).where(
                Slot.start == next_break_slot.end, Slot.space_id == space_id, Slot.work.is_(True)
            )
        )
        .scalars()
        .one_or_none()
    )
    if next_work_slot is None:
        # Likewise
        db.session.commit()
        return "", 204

    # All necessary slots exist, update the length of the break
    new_break_length = datetime.timedelta(
        minutes=times.BREAK_LENGHTS_MINS[feedback - 1]
    )
    new_break_end = next_break_slot.start + new_break_length
    db.session.execute(
        update(Slot)
        .where(Slot.slot_id == next_break_slot.slot_id, Slot.space_id == space_id)
        .values(end=next_break_slot.start + new_break_length)
    )
    db.session.execute(
        update(Slot)
        .where(Slot.slot_id == next_work_slot.slot_id, Slot.space_id == space_id)
        .values(start=new_break_end)
    )
    db.session.commit()
    return "", 204
