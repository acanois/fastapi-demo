"""API Tests"""

from uuid import uuid4

import pytest
from sqlmodel import SQLModel

from typing import Annotated

from fastapi import Depends
from fastapi.testclient import TestClient

from ..app.api import app
from ..app.database import Session, get_session
from ..app.models.user import User

client = TestClient(app)


@pytest.fixture
def db_session():
    return Annotated[Session, Depends(get_session)]

@pytest.fixture
def test_user():
    user_id = uuid4()
    new_user = {
        "user_id": str(user_id),
        "username": "test_user",
        "email": "string",
        "first_name": "test",
        "last_name": "user",
        "active": True
    }

    return new_user


def test_home():
    """Test the home page"""
    response = client.get("/")
    assert response.status_code == 200


def test_create_user(db_session, test_user):
    """Test user creation"""
    new_user = User.model_validate(user_model)

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    user_from_db = db_session.get(User, user_id=test_user["user_id"])

    assert user_from_db is not None
    assert user_from_db["user_id"] == new_user["user_id"]
