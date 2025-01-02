from datetime import timedelta
from typing import Annotated
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# When running with the fastapi command, it expects relative imports
from ..credentials import EXPIRE_TIME_MINUTES
from ..models.auth.user import User as AuthUser, users_table
from ..models.auth.auth import Token

from ..auth import (
    authenticate_user,
    get_current_active_user,
    get_current_user,
    create_access_token,
)
from ..models.auth.auth import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.get("/users/me")
async def read_users_me(current_user: Annotated[AuthUser, Depends(get_current_user)]):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[AuthUser, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(users_table, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(EXPIRE_TIME_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
