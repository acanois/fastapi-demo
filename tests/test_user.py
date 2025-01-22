"""API Tests"""

from uuid import uuid4

import pytest
from sqlmodel import Session

from typing import Annotated

from fastapi import Depends
from fastapi.testclient import TestClient

from ..app.api import app
from ..app.database import engine
from ..app.models.user import User


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def test_user(user_id):
    new_user = {
        "user_id": str(user_id),
        "username": "test_user",
        "email": "test_user@test_user.gov",
        "first_name": "test",
        "last_name": "user",
        "active": True,
    }

    return new_user


def test_create_user(test_client, test_user):
    """Test create user"""
    response = test_client.post("/user/create", json=test_user)
    assert response.status_code == 200

    new_user = response.json()

    print(new_user)

    for k in test_user.keys():
        assert test_user[k] == new_user[k]


def test_get_user(test_client):
    """Test get user"""
    test_id = 1

    response = test_client.get(f"/user/{test_id}")
    assert response.status_code == 200

