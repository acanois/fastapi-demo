"""API Tests"""

from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_home():
    """Test the home page"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "home"}
