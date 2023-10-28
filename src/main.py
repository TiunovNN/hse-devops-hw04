from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import database
from schemas import Dog, DogType, Timestamp

app = FastAPI()


# Dependency
async def get_db() -> AsyncSession:
    async with database.SessionLocal() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db)]


async def dog_db(db: DBSession):
    return database.DogRepository(db)


async def post_db(db: DBSession):
    return database.PostRepository(db)


DogDB = Annotated[database.DogRepository, Depends(dog_db)]
PostDB = Annotated[database.PostRepository, Depends(post_db)]


@app.get('/')
async def root():
    return {}


@app.post('/post')
async def get_timestamp(db: PostDB) -> Timestamp:
    return await db.create_timestamp()


@app.get('/dog')
async def get_dogs(kind: DogType, db: DogDB) -> list[Dog]:
    return await db.get_by_kind(kind)


@app.post('/dog')
async def create_dog(dog: Dog, db: DogDB) -> Dog:
    try:
        return await db.create(dog)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error)
        )


@app.get('/dog/{pk}')
async def get_dog(pk: int, db: DogDB) -> Dog:
    try:
        return await db.get_by_id(pk)
    except KeyError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'There is no dog with pk={pk}'
        )


@app.patch('/dog/{pk}')
async def update_dog(pk: int, dog: Dog, db: DogDB) -> Dog:
    try:
        return await db.update_dog(pk, dog)
    except KeyError as key_error:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(key_error)
        )
    except ValueError as value_error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(value_error)
        )
