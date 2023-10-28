from enum import Enum
from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, ConfigDict, Field


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_items=3, strict=True)
    pk: int = Field(ge=0, lt=2**31, default=None)
    kind: DogType


class Timestamp(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: int


class ErrorMessage(BaseModel):
    detail: str


DogId = Annotated[int, Path(ge=0, lt=2**31)]
