from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, func
from sqlalchemy_utils import UUIDType
from models import db


class Slot(db.Model):
    slot_id = Column(Integer, primary_key=True)
    user_id = Column(
        UUIDType(binary=True), ForeignKey("current_session.user_id"), nullable=False
    )
    # Boolean indicating whether slot is for work or a break
    work = Column(Boolean, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    # Feedback for this slot (0=satisfied, 1=neutral, 2=dissatisfied, null=ungiven)
    feedback = Column(Integer, nullable=True)
