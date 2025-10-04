from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import review_repository
from app.schemas.review_schema import Review, ReviewCreate

async def get_reviews_for_book(db: AsyncSession, book_id: int) -> List[Review]:
    """Service to retrieve all reviews for a book."""
    return await review_repository.get_reviews_by_book_id(db=db, book_id=book_id)

async def create_or_update_review(
    db: AsyncSession, book_id: int, user_id: int, review: ReviewCreate
) -> Review:
    """
    Service logic to create a new review or update an existing one
    for the given user and book.
    """
    existing_review = await review_repository.get_review_by_book_and_user(
        db=db, book_id=book_id, user_id=user_id
    )

    if existing_review:
        updated_review = await review_repository.update_review(
            db=db, db_review=existing_review, review_update=review
        )
        return updated_review
    else:
        new_review = await review_repository.create_review(
            db=db, book_id=book_id, user_id=user_id, review=review
        )
        return new_review