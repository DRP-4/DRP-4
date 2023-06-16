import datetime
import time

from flask import request, abort
from sqlalchemy import delete, update

from app import app
from models import db
from models.slot import Slot
from models.current_session import CurrentSession
from models.task import Task
from util.response import json_response
from util.user_id import with_user_id
from util.now import instant


def to_unix(date: datetime.datetime):
    return time.mktime(date.timetuple())


def do_post_session_cleanup(user_id):
    # delete any sessions that were occuring
    del_tasks = delete(Task).where(Task.user_id == user_id, Task.completed != None)
    db.session.execute(del_tasks)

    del_slot = delete(Slot).where(Slot.user_id == user_id)
    db.session.execute(del_slot)
    # don't delete the old session, so we can reuse it's settings


@app.route("/api/session/new", methods=["POST"])
@with_user_id
def start_session(user_id):
    body = request.get_json()
    if "duration" not in body:
        return "Bad Request", 400
    duration = body["duration"]
    if not isinstance(duration, int) or duration < 0:
        return "Bad Request", 400

    do_post_session_cleanup(user_id)
    # delete old session
    del_sess = delete(CurrentSession).where(CurrentSession.user_id == user_id)
    db.session.execute(del_sess)

    # add new session to the database
    start = instant()
    end = start + datetime.timedelta(minutes=duration)

    session = CurrentSession(user_id=user_id, start=start, end=end, duration=duration)
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


@app.route("/api/session/end", methods=["POST"])
@with_user_id
def end_session(user_id):
    do_post_session_cleanup(user_id)
    # outdate old session - set it's end point to now
    outdate_sess = (
        update(CurrentSession)
        .where(CurrentSession.user_id == user_id)
        .values(end=datetime.datetime.now())
    )
    db.session.execute(outdate_sess)

    db.session.commit()
    return "", 204


@app.route("/api/session/active", methods=["GET"])
@with_user_id
def is_active(user_id):
    query = (
        db.select(CurrentSession)
        .filter(CurrentSession.user_id == user_id)
        .filter(CurrentSession.end > datetime.datetime.now())
    )
    session = db.session.execute(query).scalars().first()
    return json_response({"active": session is not None})


@app.route("/api/session/current", methods=["GET"])
@with_user_id
def current_session(user_id):
    query = db.select(CurrentSession).filter(CurrentSession.user_id == user_id)
    session = db.session.execute(query).scalars().first()
    if session is None:
        return "File Not Found", 404

    session_start_unix = to_unix(session.start)
    session_end_unix = to_unix(session.end)
    duration = session.duration

    slots_query = db.select(Slot).filter(Slot.user_id == user_id)
    slots_scalar = db.session.execute(slots_query).scalars().all()

    slots = list(
        map(
            lambda slot_scalar: {
                "slot_id": slot_scalar.slot_id,
                "start_unix": to_unix(slot_scalar.start),
                "end_unix": to_unix(slot_scalar.end),
                "is_work": slot_scalar.work,
                "feedback": slot_scalar.feedback,
                "completed_tasks": list(
                    map(
                        lambda task_scalar: {
                            "name": task_scalar.title,
                            "id": task_scalar.task_id,
                            "description": task_scalar.description,
                            "complete": True,
                            "duration": task_scalar.duration_minutes,
                        },
                        db.session.execute(
                            db.select(Task).filter(
                                Task.user_id == user_id,
                                Task.completed == slot_scalar.slot_id,
                            )
                        )
                        .scalars()
                        .all(),
                    )
                ),
            },
            slots_scalar,
        )
    )

    slots.sort(key=lambda slot: slot["start_unix"])

    return json_response(
        {
            "duration": duration,
            "start_unix": session_start_unix,
            "end_unix": session_end_unix,
            "slots": slots,
        }
    )
