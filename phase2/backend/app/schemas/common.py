"""Common response schemas."""
from pydantic import BaseModel
from typing import Any, Optional


class SuccessResponse(BaseModel):
    """Standard success response wrapper."""

    data: Any
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: dict
