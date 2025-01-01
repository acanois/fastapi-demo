import os

from sqlmodel import create_engine

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]

CONNECTION_STRING = (
    f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/%s?sslmode=disable"
)
