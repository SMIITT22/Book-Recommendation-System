import pytest
from unittest.mock import AsyncMock

from app.services import auth_service, book_service, review_service
from app.models.orm_models import Book, Review
from app.schemas.review_schema import ReviewCreate

pytestmark = pytest.mark.asyncio

def test_verify_password_logic():
    """
    Unit test for the auth_service.verify_password function.
    This test has no external dependencies and is synchronous.
    """
    plain_password = "my-test-password"
    hashed_password = auth_service.pwd_context.hash(plain_password)

    assert auth_service.verify_password(plain_password, hashed_password) is True
    assert auth_service.verify_password("wrong-password", hashed_password) is False

async def test_book_service_calculates_average_rating(mocker):
    """
    Unit test for the book_service.get_all_books function.
    Verifies that the average rating logic is correct.
    """
    mock_book_with_reviews = Book(id=1, title="Book A", author="Author", genre="Genre", reviews=[Review(rating=5), Review(rating=3)])  # Avg: 4.0
    mock_book_no_reviews = Book(id=2, title="Book B", author="Author", genre="Genre", reviews=[])  # Avg: 0.0

    mocker.patch(
        "app.repositories.book_repository.get_books",
        new_callable=AsyncMock,
        return_value=[mock_book_with_reviews, mock_book_no_reviews]
    )

    result = await book_service.get_all_books(db=AsyncMock(), search=None, skip=0, limit=100)

    assert len(result) == 2
    assert result[0]["average_rating"] == 4.0
    assert result[1]["average_rating"] == 0.0

async def test_review_service_chooses_create_path(mocker):
    """
    Unit test for the 'create' path in the review_service.create_or_update_review function.
    """
    review_data = ReviewCreate(rating=5, review_text="Great book!")

    mocker.patch(
        "app.repositories.review_repository.get_review_by_book_and_user",
        new_callable=AsyncMock,
        return_value=None
    )
    mock_create_review = mocker.patch(
        "app.repositories.review_repository.create_review",
        new_callable=AsyncMock
    )
    mock_update_review = mocker.patch(
        "app.repositories.review_repository.update_review",
        new_callable=AsyncMock
    )

    await review_service.create_or_update_review(
        db=AsyncMock(), book_id=1, user_id=1, review=review_data
    )

    mock_create_review.assert_called_once()
    mock_update_review.assert_not_called()
