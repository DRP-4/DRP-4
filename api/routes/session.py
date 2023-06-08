import datetime

from flask import request
from sqlalchemy import delete

from app import app
from models import db
from models.slot import Slot
from models.current_session import CurrentSession
from models.task import Task
from util.response import json_response
from util.user_id import with_user_id


@app.route("/api/session/new", methods=["POST"])
@with_user_id
def start_session(user_id):
    body = request.get_json()

    # delete any sessions that were occuring
    del_sess = delete(CurrentSession).where(CurrentSession.user_id == user_id)
    db.session.execute(del_sess)
    del_slot = delete(Slot).where(Slot.user_id == user_id)
    db.session.execute(del_slot)

    del_tasks = delete(Task).where(
        Task.user_id == user_id and Task.completed is not Null
    )

    # add new session to the database
    start = datetime.datetime.now()
    end = start + datetime.timedelta(minutes=body["duration"])

    session = CurrentSession(user_id=user_id, start=start, end=end)
    db.session.add(session)

    # slot calculation algorithm
    # for now, just add 45-min slots followed by 15-min breaks
    # TODO: add only the first, then dynamically calculate as time goes one
    curr = start
    minute = datetime.timedelta(seconds=60)
    work_slot = 45 * minute
    break_slot = 15 * minute
    working_slot = True
    while curr != end:
        # add a new work/break slot that is upto 45/15 mins long
        slot_end = min(end, curr + (work_slot if working_slot else break_slot))
        db.session.add(
            Slot(user_id=user_id, work=working_slot, start=curr, end=slot_end)
        )
        curr = slot_end
        # if we were working, now on break, and vice-versa
        working_slot = not working_slot

    db.session.commit()

    return json_response(body)
