from http import HTTPStatus

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from deps import DogDB, PostDB
from schemas import Dog, DogId, DogType, ErrorMessage, Timestamp

app = FastAPI()


@app.get('/')
async def root():
    return {}


@app.post('/post')
async def get_post(db: PostDB) -> Timestamp:
    return await db.create()


@app.get('/dog')
async def get_dogs(db: DogDB, kind: DogType = None) -> list[Dog]:
    return await db.list(kind)


@app.post('/dog', responses={400: {'model': ErrorMessage}})
async def create_dog(dog: Dog, db: DogDB) -> Dog:
    try:
        return await db.create(dog)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error)
        )


@app.get('/dog/{pk}', responses={404: {'model': ErrorMessage}})
async def get_dog_by_pk(pk: DogId, db: DogDB) -> Dog:
    try:
        return await db.get_by_id(pk)
    except KeyError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=e.args[0]
        )


@app.patch('/dog/{pk}', responses={400: {'model': ErrorMessage}, 404: {'model': ErrorMessage}})
async def update_dog(pk: DogId, dog: Dog, db: DogDB) -> Dog:
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


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
