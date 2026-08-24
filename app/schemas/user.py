from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Incoming registration payload"""

    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    """Outgoing user profile representation"""

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT response payload"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Parsed JWT payload"""

    user_id: int | None = None
