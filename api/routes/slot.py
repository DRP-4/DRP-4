import datetime

from flask import request
from sqlalchemy import update, select

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
    if feedback < 1 or feedback > 3:
        return "Bad Request", 400

    # post feedback for session
    new_dur = (
        update(Slot)
        .where(Slot.user_id == user_id)
        .where(Slot.slot_id == slot_id)
        .values(feedback=feedback)
    )
    db.session.execute(new_dur)

    # set the break period based on feedback
    # 10 mins if reacted positively
    # 15 mins if reacted meh
    # 20 mins if reacted negatively

    # find the next break and work slot (if they exist)
    this_slot_q = (
        select(Slot).where(Slot.user_id == user_id).where(Slot.slot_id == slot_id)
    )
    this_slot = db.session.execute(this_slot_q).scalars().first()
    if this_slot is None:
        return "Bad Request - slot not found", 400
    if not this_slot.work:
        return "Bad Request - slot not a work slot", 400
    next_break_q = (
        select(Slot).where(Slot.user_id == user_id).where(Slot.start == this_slot.end)
    )
    next_break = db.session.execute(next_break_q).scalars().first()
    if next_break is not None:
        next_work_q = (
            select(Slot)
            .where(Slot.user_id == user_id)
            .where(Slot.start == next_break.end)
        )
        next_work = db.session.execute(next_work_q).scalars().first()

    # set break length based on feedback
    # feedback: 1=satisfied, 2=neutral, 3=dissatisfied, null=ungiven
    five_mins = datetime.timedelta(seconds=300)
    breaklength = five_mins + this_slot.feedback * five_mins
    breakend = this_slot.end + breaklength

    if next_break is not None:
        ch_break = (
            update(Slot).where(Slot.slot_id == next_break.slot_id).values(end=breakend)
        )
        db.session.execute(ch_break)

    if next_work is not None:
        ch_work = (
            update(Slot).where(Slot.slot_id == next_work.slot_id).values(start=breakend)
        )
        db.session.execute(ch_work)

    db.session.commit()
    return body
