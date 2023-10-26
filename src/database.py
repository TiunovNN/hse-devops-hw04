import time
from itertools import count

from src.models import Dog, DogType, Timestamp


class DogRepository:
    def __init__(self):
        self.db = {
            0: Dog(name='Bob', pk=0, kind='terrier'),
            1: Dog(name='Marli', pk=1, kind="bulldog"),
            2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
            3: Dog(name='Rex', pk=3, kind='dalmatian'),
            4: Dog(name='Pongo', pk=4, kind='dalmatian'),
            5: Dog(name='Tillman', pk=5, kind='bulldog'),
            6: Dog(name='Uga', pk=6, kind='bulldog')
        }
        self.next_id = count(7).__next__

    def get_by_kind(self, kind: DogType):
        return [
            dog
            for dog in self.db.values()
            if dog.kind == kind
        ]

    def create(self, dog: Dog) -> Dog:
        if dog.pk is not None:
            if dog.pk in self.db:
                raise ValueError(f'There is a dog with pk {dog.pk}')
        else:
            dog.pk = self.next_id()
        self.db[dog.pk] = dog
        return dog

    def get_by_id(self, pk: int) -> Dog:
        return self.db[pk]

    def update_dog(self, dog: Dog, pk: int) -> Dog:
        if pk not in self.db:
            raise KeyError(f'There is not a dog with pk = {pk}')

        if dog.pk is None:
            dog.pk = pk

        if dog.pk != pk and dog.pk in self.db:
            raise ValueError(f'There is a dog with pk {dog.pk}')

        del self.db[pk]
        self.db[pk] = dog
        return dog


class PostRepository:
    def __init__(self):
        self.db = [
            Timestamp(id=0, timestamp=12),
            Timestamp(id=1, timestamp=10)
        ]
        self.next_id = count(2).__next__

    def create_timestamp(self) -> Timestamp:
        record = Timestamp(id=self.next_id(), timestamp=int(time.time()))
        self.db.append(record)
        return record


dog_db = DogRepository()
post_db = PostRepository()


def connect():
    global dog_db
    global post_db
    dog_db = DogRepository()
    post_db = PostRepository()
