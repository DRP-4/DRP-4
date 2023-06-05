from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy_utils import UUIDType
from models import db


class Session(db.Model):
    user_id = Column(UUIDType(binary=True), primary_key=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
