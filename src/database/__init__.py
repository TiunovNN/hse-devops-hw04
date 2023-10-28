from .repository import DogRepository, PostRepository
from .session import SessionLocal

# dog_db = DogRepository()
post_db = PostRepository()


def connect():
    global dog_db
    global post_db
    # dog_db = DogRepository()
    post_db = PostRepository()
