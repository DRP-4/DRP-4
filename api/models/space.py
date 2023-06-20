from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
from models import db


class Space(db.Model):
    space_id = Column(UUIDType(binary=True), nullable=False, primary_key=True)
    display_name = Column(String, nullable=False)
