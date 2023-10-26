import time
from http import HTTPStatus

import pytest
from httpx import AsyncClient
from anys import ANY_INT

from src.main import app, DogType

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


class TestDogs:
    @pytest.mark.parametrize('kind', list(DogType))
    async def test_get_list(self, client: AsyncClient, kind):
        response = await client.get('/dog', params={'kind': kind.value})
        assert response.status_code == HTTPStatus.OK, response.text
        dogs = response.json()
        assert len(dogs) > 0
        assert all(dog['kind'] == kind.value for dog in dogs)

    async def test_wrong_kind(self, client: AsyncClient):
        response = await client.get('/dog', params={'kind': 'wrong_kind'})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        body = response.json()
        assert body == {
            'detail': [{
                'ctx': {'expected': "'terrier', 'bulldog' or 'dalmatian'"},
                'input': 'wrong_kind',
                'loc': ['query', 'kind'],
                'msg': "Input should be 'terrier', 'bulldog' or 'dalmatian'",
                'type': 'enum'
            }]
        }

    async def test_create(self, client: AsyncClient):
        new_dog = {
            'name': 'fluffy',
            'kind': DogType.dalmatian,
        }
        response = await client.post('/dog', json=new_dog)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body == {
            'name': 'fluffy',
            'kind': DogType.dalmatian,
            'pk': ANY_INT,
        }

    async def test_create_with_pk(self, client: AsyncClient):
        new_dog = {
            'name': 'fluffy',
            'pk': 1000,
            'kind': DogType.dalmatian,
        }
        response = await client.post('/dog', json=new_dog)
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert body == new_dog

    async def test_create_wrong_dog(self, client: AsyncClient):
        new_dog = {
            'pk': 1000,
        }
        response = await client.post('/dog', json=new_dog)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        body = response.json()
        assert body == {
            'detail': [
                {
                    'input': {'pk': 1000},
                    'loc': ['body', 'name'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing',
                },
                {
                    'input': {'pk': 1000},
                    'loc': ['body', 'kind'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing'
                }
            ]
        }

    async def test_create_non_unique_pk(self, client: AsyncClient):
        new_dog = {
            'name': 'fluffy',
            'pk': 1002,
            'kind': DogType.dalmatian,
        }
        response = await client.post('/dog', json=new_dog)
        assert response.status_code == HTTPStatus.OK
        response = await client.post('/dog', json=new_dog)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {'detail': 'There is an object with pk 1002'}
