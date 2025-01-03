"""API Main"""

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse


from sqlmodel import Session

from .routers import auth, user

from .database import get_session, bootstrap_db


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def home():
    message = {"message": "home"}

    return JSONResponse(message)
