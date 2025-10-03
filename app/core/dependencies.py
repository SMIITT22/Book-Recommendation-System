from app.core.database import AsyncSessionLocal

async def get_db():
    """
    Dependency that provides an async database session per request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()