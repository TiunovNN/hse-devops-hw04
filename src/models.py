from enum import Enum

from pydantic import BaseModel


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int | None = None
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int
