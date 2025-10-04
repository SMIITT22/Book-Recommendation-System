from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import book_repository

async def get_all_books(db: AsyncSession, search: Optional[str], skip: int, limit: int) -> List[dict]:
    """
    Service to get all books and dynamically calculate the average rating.
    """
    books = await book_repository.get_books(db, search, skip, limit)
    
    book_list = []
    for book in books:
        if book.reviews:
            avg_rating = sum(r.rating for r in book.reviews) / len(book.reviews)
        else:
            avg_rating = 0.0
        
        book_list.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "average_rating": round(avg_rating, 1)
        })
        
    return book_list