from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


@cache
def async_engine():
    return create_async_engine(settings().DATABASE_URL, echo=True)


@cache
def async_session():
    return sessionmaker(
        expire_on_commit=False,
        class_=AsyncSession,
        bind=async_engine(),
    )()


@cache
def sync_engine():
    return create_engine(settings().SYNC_DATABASE_URL, echo=True)
