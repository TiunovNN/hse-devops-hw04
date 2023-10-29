from sqlalchemy import Column, Enum, Identity, Integer, String

from schemas import DogType
from .base_class import Base


class DogModel(Base):
    __tablename__ = 'dogs'

    pk = Column(
        Integer,
        Identity(start=0, minvalue=0, cycle=True),
        primary_key=True,
        index=True,
    )
    name = Column(String(100))
    kind = Column(Enum(DogType), index=True)


class TimestampModel(Base):
    __tablename__ = 'timestamps'

    id = Column(
        Integer,
        Identity(start=0, minvalue=0, cycle=True),
        primary_key=True,
        index=True,
    )
    timestamp = Column(Integer)
