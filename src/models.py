# models.py
# PostgreSQL에 저장할 Table의 구성을 지정하는 모듈

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String(length=11), nullable=False)
    # groups = relationship("Group", back_populates="users")


"""
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    users = relationship("User", back_populates="groups")
"""
