from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.orm_models import Review
from app.schemas.review_schema import ReviewCreate

async def get_reviews_by_book_id(db: AsyncSession, book_id: int) -> List[Review]:
    """Fetches all reviews for a specific book from the database."""
    query = select(Review).where(Review.book_id == book_id)
    result = await db.execute(query)
    return result.scalars().all()

async def get_review_by_book_and_user(db: AsyncSession, book_id: int, user_id: int) -> Optional[Review]:
    """Fetches a single review for a book by a specific user."""
    query = select(Review).where(Review.book_id == book_id, Review.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().first()

async def create_review(db: AsyncSession, book_id: int, user_id: int, review: ReviewCreate) -> Review:
    """Creates a new review record in the database."""
    db_review = Review(**review.model_dump(), book_id=book_id, user_id=user_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def update_review(db: AsyncSession, db_review: Review, review_update: ReviewCreate) -> Review:
    """Updates an existing review record in the database."""
    db_review.rating = review_update.rating
    db_review.review_text = review_update.review_text
    await db.commit()
    await db.refresh(db_review)
    return db_review