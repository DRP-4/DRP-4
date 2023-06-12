from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    func,
)
from sqlalchemy_utils import UUIDType
from models import db


class Task(db.Model):
    task_id = Column(Integer, primary_key=True)
    user_id = Column(UUIDType(binary=True), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Integer, ForeignKey("slot.slot_id"), nullable=True)
    created = Column(DateTime, server_default=func.now())
    # Easier to keep this around as an integer
    duration_minutes = Column(Integer, nullable=True)
