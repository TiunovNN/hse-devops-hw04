from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import database


async def get_db() -> AsyncSession:
    async with database.async_session() as session:
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db)]


async def dog_db(db: DBSession):
    return database.DogRepository(db)


async def post_db(db: DBSession):
    return database.PostRepository(db)


DogDB = Annotated[database.DogRepository, Depends(dog_db)]
PostDB = Annotated[database.PostRepository, Depends(post_db)]
