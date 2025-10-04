from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.schemas import book_schema
from app.services import book_service

router = APIRouter()

@router.get("/", response_model=List[book_schema.Book])
async def read_books(
    search: Optional[str] = Query(None, description="Search by title or author"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Limit for pagination"),
    db: AsyncSession = Depends(get_db),
    # This dependency protects the endpoint.
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a list of all books. Requires a valid JWT token.
    Supports search by title/author and pagination (skip/limit).
    """
    books = await book_service.get_all_books(db, search=search, skip=skip, limit=limit)
    return books