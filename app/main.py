import json
from fastapi import FastAPI
from app.core.database import engine, Base, AsyncSessionLocal
from app.models import orm_models
from sqlalchemy.future import select
from app.api.v1 import auth, books, reviews

# initialize FastAPI app
app = FastAPI(title="Book Recommendation System API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(orm_models.Book))
            if not result.scalars().first():
                print("--- Seeding book data into the database ---")
                with open("books.json", "r") as f:
                    books_data = json.load(f)
                    for book_item in books_data:
                        book = orm_models.Book(**book_item)
                        session.add(book)
                await session.commit()

# to check if the API is running
@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to the Book Recommendation System API!"}

# Add the login router
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

# Add the books router
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])

# Add the reviews router
app.include_router(reviews.router, prefix="/api/v1", tags=["Reviews"])
