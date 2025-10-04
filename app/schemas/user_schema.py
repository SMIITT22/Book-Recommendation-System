from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True