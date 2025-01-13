"""USER Router"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..database import get_session
from ..models.user import User, AllUsers

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


@router.get("/users", response_model=AllUsers)
def get_all_users(
    session: session,
    # offset: int = 0,
    # limit: Annotated[int, Query(le=100)] = 100,
):
    query = """SELECT * FROM user;"""
    users = session.exec(query)

    return users


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


@router.get("/delete/{user_id}")
def delete_user(user_id: str | int, session: session):
    """Get a single user by id

    Args:
        user_id (int): The user id to query
        session (Annotated[Session, Depends): Session object for the transaction

    Raises:
        HTTPException: 404 if user not found

    Returns:
        user: User found by id
    """
    user = session.delete(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
