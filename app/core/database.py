from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

# this gives us the url for the async database connection
engine = create_async_engine(settings.ASYNC_DATABASE_URL)

# for sessions to interact with the database
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# this is the base class for our ORM models
Base = declarative_base()