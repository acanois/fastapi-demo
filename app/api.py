"""API"""

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse


from sqlmodel import SQLModel, Session, create_engine

from .routers import auth

from .database import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)


def bootstrap_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)


@app.get("/")
async def home():
    message = {"message": "home"}

    return JSONResponse(message)
