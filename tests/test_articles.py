import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai import get_ai_rate_data

@pytest.fixture(scope="module")
def client():
    """ Фікстура для створення TestClient. """
    with TestClient(app) as c:
        yield c

@pytest.fixture
def article_payload():
    """ Фікстура, що повертає дані для створення article. """
    payload = {
        "id": 2,
        "name": "Test Article",
        "body": "Test Article Body",
        "user_id": 1
    }
    return payload

@pytest.fixture()
def existing_article_payload():
    payload = {
        "id": 1,
        "name": "Test Article",
        "body": "Test Article Body",
        "user_id": 1
    }
    return payload

@pytest.fixture()
def django_article_payload():
    payload = {
        "id": 1,
        "name": "Test Django Article",
        "body": "Test Article Body",
        "user_id": 1
    }
    return payload

# GET ARTICLES TESTING

def test_get_articles_list(client):
    response = client.get("api/articles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_existing_article(client, existing_article_payload):
    article_id = existing_article_payload.get("id")
    response = client.get(f"api/article/{article_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_nonexisting_article(client, article_payload):
    article_id = article_payload.get("id")
    response = client.get(f"api/article/{article_id}")
    assert response.status_code == 404

# CREATE ARTICLES TESTING

def test_create_article(client, article_payload):
    response = client.post("api/article/", json=article_payload)
    assert response.status_code == 201

# def test_create_existing_article(client, existing_article_payload):
#     response = client.post("api/article/", json=existing_article_payload)
#     assert response.status_code == 422

def test_create_django_validation_article(client, django_article_payload):
    response = client.post("api/article/", json=django_article_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Django can`t be in article name"

@pytest.mark.asyncio
@patch("app.services.ai.httpx.AsyncClient")
async def test_ai_rating_five_mocked(mock_client_cls, article_payload):
    mock_response_payload = {"rate": 5}

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_payload

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_client_cls.return_value.__aenter__.return_value = mock_client

    result = await get_ai_rate_data(article_payload.get("body"))
    mock_client.get.assert_called_once_with("https://api.openai.com/gpt-4o-mini/", article_payload.get("body"))
    assert result == mock_response_payload