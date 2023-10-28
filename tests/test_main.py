import time
from copy import copy
from http import HTTPStatus

import pytest
from anys import ANY_INT
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database import DogModel, TimestampModel
from database.base_class import Base
from deps import get_db
from main import app
from schemas import DogType

pytestmark = pytest.mark.anyio


@pytest.fixture()
async def db_session() -> AsyncSession:
    engine = create_async_engine('sqlite+aiosqlite://', echo=True)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        TestingSessionLocal = sessionmaker(
            expire_on_commit=False,
            class_=AsyncSession,
            bind=engine,
        )
        async with TestingSessionLocal(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture()
async def prepare_data(db_session):
    dogs = [
        DogModel(name='Bob', pk=0, kind='terrier'),
        DogModel(name='Marli', pk=1, kind="bulldog"),
        DogModel(name='Snoopy', pk=2, kind='dalmatian'),
        DogModel(name='Rex', pk=3, kind='dalmatian'),
        DogModel(name='Pongo', pk=4, kind='dalmatian'),
        DogModel(name='Tillman', pk=5, kind='bulldog'),
        DogModel(name='Uga', pk=6, kind='bulldog'),
    ]
    timestamps = [
        TimestampModel(id=0, timestamp=12),
        TimestampModel(id=1, timestamp=10)
    ]
    db_session.add_all(dogs)
    db_session.add_all(timestamps)
    await db_session.commit()


@pytest.fixture
async def client(db_session, prepare_data):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
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
    print('Post1')
    resp1 = await client.post("/post")
    print('Post2')
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
        assert response.json() == {'detail': 'There is a dog with pk 1002'}

    async def test_get_by_id(self, client: AsyncClient):
        response = await client.get('/dog/0')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'name': 'Bob', 'pk': 0, 'kind': 'terrier'}

    async def test_get_by_id_not_found(self, client: AsyncClient):
        response = await client.get('/dog/9999')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'There is not a dog with pk=9999'}

    async def test_update_dog(self, client: AsyncClient):
        dog_list_response = await client.get('/dog', params={'kind': DogType.terrier.value})
        dog_list = dog_list_response.json()
        dog = copy(dog_list[0])
        pk = dog['pk']
        dog['name'] = 'unusual_name'

        response = await client.patch(f'/dog/{pk}', json=dog)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == dog
        new_dog_response = await client.get(f'/dog/{pk}')
        new_dog = new_dog_response.json()
        assert new_dog != dog_list[0]
        assert new_dog == dog

    async def test_update_dog_without_pk(self, client: AsyncClient):
        dog_list_response = await client.get('/dog', params={'kind': DogType.terrier.value})
        dog_list = dog_list_response.json()
        dog = copy(dog_list[0])
        pk = dog.pop('pk')
        dog['name'] = 'unusual_name'

        response = await client.patch(f'/dog/{pk}', json=dog)
        dog['pk'] = pk
        assert response.status_code == HTTPStatus.OK
        assert response.json() == dog
        new_dog_response = await client.get(f'/dog/{pk}')
        new_dog = new_dog_response.json()
        assert new_dog != dog_list[0]
        assert new_dog == dog
