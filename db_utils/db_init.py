from db_utils.base import Base
from db_utils.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)
