"""Auth functions"""

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
import jwt
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

from app.models.auth import TokenData

from .models.user import User, UserInDB, users_table

from .credentials import FAKE_SECRET_KEY

ALGORITHM = "HS256"

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _verify_password(password, hashed_password):
    """Verifies a password against an existing password hash

    Args:
        password (str): User-supplied password
        hashed_password (str): Existing password hash

    Returns:
        bool: True if password matches hashed_password
    """
    return crypt_context.verify(password, hashed_password)


def get_user(db, username: str):
    """Temp. Will be replaced with a database query."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    """Temp. Will be replaced with a database query."""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not _verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, FAKE_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, FAKE_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(users_table, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
