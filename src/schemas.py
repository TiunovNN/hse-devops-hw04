from enum import Enum

from pydantic import BaseModel, ConfigDict


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    pk: int | None = None
    kind: DogType


class Timestamp(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: int