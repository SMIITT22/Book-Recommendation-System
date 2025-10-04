from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1 import auth

# initialize FastAPI app
app = FastAPI(title="Book Recommendation System API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# to check if the API is running
@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to the Book Recommendation System API!"}

# login route
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
