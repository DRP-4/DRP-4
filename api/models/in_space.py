from sqlalchemy import Column, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy_utils import UUIDType
from models import db


class InSpace(db.Model):
    __table_args__ = (UniqueConstraint("space_id", "user_id"),)
    space_id = Column(
        ForeignKey("space.space_id"), UUIDType(binary=True), nullable=False
    )
    user_id = Column(UUIDType(binary=True), nullable=False)
    is_owner = Column(Boolean, nullable=False)
    __mapper_args__ = {"primary_key": [space_id, user_id]}
