from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy_utils import UUIDType
from models import db


class Slot(db.Model):
    slot_id = Column(Integer, primary_key=True)
    user_id = Column(
        UUIDType(binary=True), ForeignKey("session.user_id"), nullable=False
    )
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
