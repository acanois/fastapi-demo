"""DATABASE functionality"""

import os

from sqlmodel import SQLModel, Session, create_engine

DB_USER = os.environ["DB_USER"]
DB_NAME = os.environ["DB_NAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

CONNECTION_STRING = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"
)

engine = create_engine(CONNECTION_STRING)


def bootstrap_db():
    """Creates all tables in the database"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Yields a session object for a database transaction"""
    with Session(engine) as session:
        yield session
