from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Time,
    Boolean,
    func,
)
from sqlalchemy_utils import UUIDType
from models import db


class Task(db.Model):
    task_id = Column(Integer, primary_key=True)
    user_id = Column(
        UUIDType(binary=True), ForeignKey("current_session.user_id"), nullable=False
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False)
    created = Column(DateTime, server_default=func.now())
    duration = Column(Time, nullable=False)
