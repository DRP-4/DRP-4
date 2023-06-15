from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy_utils import UUIDType
from models import db


class CurrentSession(db.Model):
    user_id = Column(UUIDType(binary=True), primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    # duration of the session in minutes
    # so we can end the session early without losing how long it was meant to be
