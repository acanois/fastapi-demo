"""Auth functions"""

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

from .models.user import UserInDB


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
