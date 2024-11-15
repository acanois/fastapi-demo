from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(password, hashed_password):
    """Verifies a password against an existing password hash

    Args:
        password (str): User-supplied password
        hashed_password (str): Existing password hash

    Returns:
        bool: True if password matches hashed_password
    """
    return crypt_context.verify(password, hashed_password)


