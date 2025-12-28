"""Pydantic models for Todo CLI Application."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Data transfer object for creating new tasks."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate that title is not empty after stripping whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        return stripped


class TaskUpdate(BaseModel):
    """Data transfer object for updating existing tasks."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty_if_provided(cls, v: str | None) -> str | None:
        """Validate that title is not empty after stripping whitespace if provided."""
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Title cannot be empty")
            return stripped
        return v


class Task(BaseModel):
    """Domain model representing a single todo item."""

    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"frozen": False}
