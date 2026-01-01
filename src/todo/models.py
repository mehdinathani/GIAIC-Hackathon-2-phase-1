"""Pydantic models for Todo CLI Application."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class PriorityEnum(str, Enum):
    """Priority levels for tasks."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RecurrenceEnum(str, Enum):
    """Recurrence rules for tasks."""

    NONE = "NONE"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


class TaskCreate(BaseModel):
    """Data transfer object for creating new tasks."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    priority: PriorityEnum = Field(default=PriorityEnum.LOW)
    tags: list[str] = Field(default_factory=list)
    due_date: datetime | None = Field(default=None)
    recurrence: RecurrenceEnum = Field(default=RecurrenceEnum.NONE)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate that title is not empty after stripping whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        return stripped

    @field_validator("tags")
    @classmethod
    def tags_must_start_with_hash(cls, tags: list[str]) -> list[str]:
        """Validate that each tag starts with a '#'."""
        for tag in tags:
            if not tag.startswith("#"):
                raise ValueError(f"Tag '{tag}' must start with '#'")
        return tags


class TaskUpdate(BaseModel):
    """Data transfer object for updating existing tasks."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = Field(default=None)
    priority: PriorityEnum | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
    due_date: datetime | None = Field(default=None)
    recurrence: RecurrenceEnum | None = Field(default=None)

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

    @field_validator("tags")
    @classmethod
    def tags_must_start_with_hash_if_provided(cls, tags: list[str] | None) -> list[str] | None:
        """Validate that each tag starts with a '#' if provided."""
        if tags is not None:
            for tag in tags:
                if not tag.startswith("#"):
                    raise ValueError(f"Tag '{tag}' must start with '#'")
        return tags


class Task(BaseModel):
    """Domain model representing a single todo item."""

    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: PriorityEnum = Field(default=PriorityEnum.LOW)
    tags: list[str] = Field(default_factory=list)
    due_date: datetime | None = Field(default=None)
    recurrence: RecurrenceEnum = Field(default=RecurrenceEnum.NONE)
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"frozen": False}
