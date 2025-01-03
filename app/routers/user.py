"""USER Router"""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..models.user import User


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create")
def create_user(user: User, session: Annotated[Session, Depends(get_session)]):
    """Create a new user

    Args:
        user (User): User to add to the database
        session (Annotated[Session, Depends): Session object for the transaction

    Returns:
        User: User added to the database
    """
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
