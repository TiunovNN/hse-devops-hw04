from http import HTTPStatus
from itertools import count

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

import database
from models import Dog, DogType, Timestamp

app = FastAPI()

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


@app.on_event('startup')
async def startup_event():
    database.connect()


@app.get('/')
async def root():
    return {}


@app.post('/post')
async def get_timestemp() -> Timestamp:
    return database.post_db.create_timestamp()


@app.get('/dog')
async def get_dogs(kind: DogType) -> list[Dog]:
    return database.dog_db.get_by_kind(kind)


@app.post('/dog')
async def create_dog(dog: Dog) -> Dog:
    try:
        return database.dog_db.create(dog)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error)
        )


@app.get('/dog/{pk}')
async def get_dog(pk: int) -> Dog:
    try:
        return database.dog_db.get_by_id(pk)
    except KeyError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'There is no dog with pk={pk}'
        )


@app.get('/dog/{pk}')
async def update_dog(pk: int) -> Dog:
    try:
        return database.dog_db.get_by_id(pk)
    except KeyError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'There is no dog with pk={pk}'
        )
