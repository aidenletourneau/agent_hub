from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    name: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True