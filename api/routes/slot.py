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

    # check this slot is ours, and that the end has passed
    new_dur = (
        update(Slot)
        .where(Slot.user_id == user_id)
        .where(Slot.slot_id == slot_id)
        .values(feedback=feedback)
    )
    db.session.execute(new_dur)

    # if the session went badly or well, adjust the break period
    # add on 5 minutes if reacted poorly, take off 5 mins if good
    # adjust session after as well
    if feedback == 1 or feedback == 3:
        # get this slots end time
        this_slot_q = (
            select(Slot).where(Slot.user_id == user_id).where(Slot.slot_id == slot_id)
        )
        this_slot = db.session.execute(this_slot_q).scalars().first()
        next_break_q = (
            select(Slot)
            .where(Slot.user_id == user_id)
            .where(Slot.start == this_slot.end)
        )
        next_break = db.session.execute(next_break_q).scalars().first()
        next_work_q = (
            select(Slot)
            .where(Slot.user_id == user_id)
            .where(Slot.start == next_break.end)
        )
        next_work = db.session.execute(next_work_q).scalars().first()

        # satisfied is 1, dissatisfied is 3
        satis_delta = datetime.timedelta(seconds=600)
        if next_break is not None:
            ch_break = (
                update(Slot)
                .where(Slot.slot_id == next_break.slot_id)
                .values(
                    end=(
                        (next_break.end - satis_delta)
                        if (feedback == 1)
                        else (next_break.end + satis_delta)
                    )
                )
            )
            db.session.execute(ch_break)
        if next_work is not None:
            ch_work = (
                update(Slot)
                .where(Slot.slot_id == next_work.slot_id)
                .values(
                    start=(
                        (next_work.start - satis_delta)
                        if (feedback == 1)
                        else (next_work.start + satis_delta)
                    )
                )
            )
            db.session.execute(ch_work)

    db.session.commit()

    return body
