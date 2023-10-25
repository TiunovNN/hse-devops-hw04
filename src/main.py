import time
from enum import Enum
from itertools import count

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.v1 import PydanticValueError

app = FastAPI()


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


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}
dogs_next_id = count(7).__next__

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]
post_next_id = count(2).__next__


class PKNonUniqueError(PydanticValueError):
    code = 'pk.non_unique'
    msg_template = 'There is an object with pk {pk}'


@app.get('/')
async def root():
    return {}


@app.post('/post')
async def get() -> Timestamp:
    return Timestamp(id=post_next_id(), timestamp=int(time.time()))

@app.get('/dog')
async def dogs(kind: DogType) -> list[Dog]:
    return [
        dog
        for dog in dogs_db.values()
        if dog.kind == kind
    ]

@app.post('/dog')
async def create_dog(dog: Dog) -> Dog:
    if dog.pk is not None:
        if dog.pk in dogs_db:
            raise RequestValidationError(
                errors=[
                    ErrorWrapper(
                        PKNonUniqueError(pk=dog.pk),
                        loc=['body', 'pk'],
                    ),
                ],
            )
    else:
        dog.pk = dogs_next_id()
    dogs_db[dog.pk] = dog
    return dog
