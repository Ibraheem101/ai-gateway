from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    """Incoming prompt request"""

    prompt: str = Field(min_length=1)
    provider: str = Field(default="gemini")
    model: str | None = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0)


class InferenceResponse(BaseModel):
    """Unified response payload"""

    content: str
    provider: str
    model: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    cached: bool = Field(default=False)
