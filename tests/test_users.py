import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    """ Фікстура для створення TestClient. """
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def get_valid_token(client):
    response = client.post("/auth/login", data={"username": "Vitaliy", "password": "qwerty"})
    return response.json()["access_token"]

def test_unauthorised_get_current_user(client):
    response = client.get("/auth/users/me")
    assert response.status_code == 401

def test_access_protected_route_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get("/auth/users/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_get_current_user(client, get_valid_token):
    headers = {"Authorization": f"Bearer {get_valid_token}"}
    response = client.get("/auth/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["sub"] == "Vitaliy"

