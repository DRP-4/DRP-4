from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, func
from sqlalchemy_utils import UUIDType
from models import db


class Slot(db.Model):
    slot_id = Column(Integer, primary_key=True)
    space_id = Column(
        UUIDType(binary=True), ForeignKey("current_session.space_id"), nullable=False
    )
    # Boolean indicating whether slot is for work or a break
    work = Column(Boolean, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    # Feedback for this slot (1=satisfied, 2=neutral, 3=dissatisfied, null=ungiven)
    feedback = Column(Integer, nullable=True)
