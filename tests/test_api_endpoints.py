import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock

from app.main import app
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.user_schema import User
from app.models.orm_models import Book, Review

async def override_get_db():
    """Mock dependency for the database session."""
    yield AsyncMock()

async def override_get_current_user():
    """Mock dependency for the authenticated user."""
    return User(id=1, username="testuser", email="test@example.com")

# Apply the overrides to the main FastAPI app instance for all tests.
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Mark all tests in this file as asynchronous
pytestmark = pytest.mark.asyncio


async def test_read_books_endpoint(mocker):
    """
    Tests the GET /books endpoint, mocking the repository layer.
    """
    mock_book = Book(id=1, title="Test Book", author="Author", genre="Genre", reviews=[Review(rating=5), Review(rating=3)])
    mocker.patch("app.repositories.book_repository.get_books", new_callable=AsyncMock, return_value=[mock_book])

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/books/")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["title"] == "Test Book"
    assert response_data[0]["average_rating"] == 4.0

async def test_create_review_endpoint(mocker):
    """
    Tests the POST /books/{book_id}/reviews endpoint for creating a new review.
    """
    review_payload = {"rating": 5, "review_text": "A masterpiece!"}
    
    mocker.patch("app.repositories.review_repository.get_review_by_book_and_user", new_callable=AsyncMock, return_value=None)
    
    mock_created_review = Review(id=1, book_id=1, user_id=1, **review_payload)
    mocker.patch("app.repositories.review_repository.create_review", new_callable=AsyncMock, return_value=mock_created_review)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/books/1/reviews", json=review_payload)

    assert response.status_code == 201
    assert response.json()["review_text"] == "A masterpiece!"
    assert response.json()["rating"] == 5

async def test_update_review_endpoint(mocker):
    """
    Tests the POST /books/{book_id}/reviews endpoint for updating an existing review.
    """
    review_payload = {"rating": 4, "review_text": "Updated review."}
    
    existing_review = Review(id=99, book_id=1, user_id=1, rating=3, review_text="Old text")
    mocker.patch("app.repositories.review_repository.get_review_by_book_and_user", new_callable=AsyncMock, return_value=existing_review)
    
    mock_updated_review = Review(id=99, book_id=1, user_id=1, **review_payload)
    mocker.patch("app.repositories.review_repository.update_review", new_callable=AsyncMock, return_value=mock_updated_review)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/books/1/reviews", json=review_payload)
    
    assert response.status_code == 201
    assert response.json()["review_text"] == "Updated review."
    assert response.json()["rating"] == 4