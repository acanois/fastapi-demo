"""API Tests"""

from uuid import uuid4

import pytest
from sqlmodel import SQLModel, Session

from fastapi.testclient import TestClient

from ..app.api import app
from ..app.database import engine, get_session

SQLModel.metadata.create_all(engine)

@pytest.fixture
def test_client():

    def test_session():
        with Session(engine) as session:
            yield session
            session.rollback()

    app.dependency_overrides[get_session] = test_session

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

    for k in test_user.keys():
        assert test_user[k] == new_user[k]


def test_get_user(test_client):
    """Test get user"""
    test_id = 1

    response = test_client.get(f"/user/{test_id}")
    assert response.status_code == 200
