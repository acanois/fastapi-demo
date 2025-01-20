"""USER Router"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import get_session
from ..models.user import User

session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: int, session: session):
    """Get a single user by id

    Args:
        user_id (int): The user id to query
        session (Annotated[Session, Depends): Session object for the transaction

    Raises:
        HTTPException: 404 if user not found

    Returns:
        user: User found by id
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/create", response_model=User)
def create_user(user: User, session: session):
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


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, session: session):
    """Get a single user by id

    Args:
        user_id (int): The user id to query
        session (Annotated[Session, Depends): Session object for the transaction

    Raises:
        HTTPException: 404 if user not found

    Returns:
        user: User found by id
    """

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)

    return user
