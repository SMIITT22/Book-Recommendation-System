from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    average_rating: float

    class Config:
        from_attributes = True