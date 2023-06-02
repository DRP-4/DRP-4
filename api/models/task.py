from sqlalchemy import Column, Integer, String, DateTime, func
from models import db

class Task(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now())
