from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional

# Schema for creating a new user (input)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for reading user data (output)
class User(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    total_xp: int
    current_level: int

    class Config:
        from_attributes = True # Changed from orm_mode for Pydantic v2

# Schema for the access token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for the data embedded in the token
class TokenData(BaseModel):
    username: Optional[str] = None
