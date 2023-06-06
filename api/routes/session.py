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


@app.route("/api/startSession", methods=["POST"])
@with_user_id
def start_session(user_id):
    body = request.get_json()

    del_sess = delete(CurrentSession).where(CurrentSession.user_id == user_id)
    db.session.execute(del_sess)
    del_slot = delete(Slot).where(Slot.user_id == user_id)
    db.session.execute(del_slot)

    start = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(minutes=body["duration"])

    session = CurrentSession(user_id=user_id, start=start, end=end)
    db.session.add(session)

    for title in body["tasks"]:
        task = Task(
            title=title,
            user_id=user_id,
        )
        db.session.add(task)

    db.session.commit()

    return json_response(body)
