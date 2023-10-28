from sqlalchemy import Column, Enum, Integer, String

from schemas import DogType
from .base_class import Base


class DogModel(Base):
    __tablename__ = 'dogs'

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    kind = Column(Enum(DogType))


class TimestampModel(Base):
    __tablename__ = 'timestamps'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Integer)
