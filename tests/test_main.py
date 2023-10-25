import time

import pytest
from httpx import AsyncClient
from anys import ANY_INT

from src.main import app  # inited FastAPI app

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


async def test_get_root(client: AsyncClient):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {}


async def test_post_get(client: AsyncClient):
    resp = await client.post("/post")
    assert resp.status_code == 200
    assert resp.json() == {
        'id': ANY_INT,
        'timestamp': pytest.approx(int(time.time()), abs=2),
    }


async def test_unique_timestamp_id(client: AsyncClient):
    resp1 = await client.post("/post")
    resp2 = await client.post("/post")
    assert resp1.json()['id'] != resp2.json()['id']
