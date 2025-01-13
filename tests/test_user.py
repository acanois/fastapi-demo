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


@pytest.fixture
def db_session():
    return Annotated[Session, Depends(get_session)]


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
        "email": "string",
        "first_name": "test",
        "last_name": "user",
        "active": True,
    }

    return new_user


def test_home(test_client):
    """Test the home page"""
    response = test_client.get("/")
    assert response.status_code == 200


def test_create_user(test_client, test_user):
    """Test create user"""
    create_res = test_client.post("/user/create", json=test_user)
    assert create_res.status_code == 200

    create_json = create_res.json()
    create_id = create_json["id"]

    get_res = test_client.get(f"/user/{create_id}")
    assert get_res.status_code == 200

    get_json = get_res.json()
    get_id = get_json["id"]
    assert get_id == create_id


def test_get_all_users(test_client):
    """Test get all users"""
    response = test_client.get("/user/users")

    assert response.status_code == 200

