from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreate(BaseModel):
    """Incoming request payload"""

    name: str


class ApiKeyRead(BaseModel):
    """Outgoing metadata list representation"""

    id: int
    name: str = Field(min_length=1, max_length=100)
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreatedResponse(ApiKeyRead):
    """One-time response returned only at key creation time"""

    api_key: str  # The raw unhashed API key string returned once to the user
