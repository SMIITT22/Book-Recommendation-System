from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas import review_schema, user_schema
from app.services import review_service

router = APIRouter()

@router.get("/books/{book_id}/reviews", response_model=List[review_schema.Review])
async def get_reviews_for_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all reviews for a specific book. This is a public endpoint.
    """
    reviews = await review_service.get_reviews_for_book(db, book_id=book_id)
    return reviews

@router.post(
    "/books/{book_id}/reviews",
    response_model=review_schema.Review,
    status_code=status.HTTP_201_CREATED
)
async def create_or_update_book_review(
    book_id: int,
    review: review_schema.ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    """
    Create a new review for a book or update an existing one.
    Requires authentication.
    """
    created_review = await review_service.create_or_update_review(
        db=db, book_id=book_id, user_id=current_user.id, review=review
    )
    return created_review