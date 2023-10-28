import time

from pydantic import TypeAdapter
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Dog, DogType, Timestamp
from .models import DogModel, TimestampModel


class DogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_kind(self, kind: DogType) -> list[Dog]:
        statement = (
            select(DogModel)
            .where(DogModel.kind == kind)
            .order_by(DogModel.pk.desc())
        )
        result = await self.db.execute(statement)
        return TypeAdapter(list[Dog]).validate_python(result.scalars().all())

    async def create(self, dog: Dog) -> Dog:
        db_dog = DogModel(
            pk=dog.pk,
            name=dog.name,
            kind=dog.kind,
        )
        self.db.add(db_dog)
        try:
            await self.db.commit()
            await self.db.refresh(db_dog)
        except IntegrityError:
            raise ValueError(f'There is a dog with pk {dog.pk}')

        return TypeAdapter(Dog).validate_python(db_dog)

    async def get_by_id(self, pk: int) -> Dog:
        statement = select(DogModel).where(DogModel.pk == pk)
        result = await self.db.execute(statement)
        try:
            return TypeAdapter(Dog).validate_python(result.scalar_one())
        except NoResultFound:
            raise KeyError(f'There is not a dog with pk = {pk}')

    async def update_dog(self, pk: int, dog: Dog) -> Dog:
        statement = (
            update(DogModel)
            .values(dog.model_dump())
            .where(DogModel.pk == pk)
        )

        await self.db.execute(statement)
        await self.db.commit()
        return await self.get_by_id(dog.pk)


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self) -> Timestamp:
        record = TimestampModel(timestamp=int(time.time()))
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return TypeAdapter(Timestamp).validate_python(record)
