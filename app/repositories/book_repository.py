from typing import List, Optional
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.orm_models import Book

async def get_books(db: AsyncSession, search: Optional[str], skip: int, limit: int) -> List[Book]:
    """
    Retrieves a list of books from the database.
    Includes search by title/author and pagination.
    """
    query = select(Book).options(selectinload(Book.reviews)).order_by(Book.id)
    
    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%")
            )
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().unique().all()