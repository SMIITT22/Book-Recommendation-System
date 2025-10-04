from pydantic import BaseModel, constr, conint
from typing import Optional

class ReviewCreate(BaseModel):
    rating: conint(ge=1, le=5)
    review_text: Optional[constr(max_length=1000)] = None

class Review(BaseModel):
    id: int
    book_id: int
    user_id: int
    rating: int
    review_text: Optional[str] = None

    class Config:
        from_attributes = True