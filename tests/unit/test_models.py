"""Unit tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from todo.models import PriorityEnum, Task, TaskCreate, TaskUpdate


class TestTaskCreate:
    """Tests for TaskCreate model validation."""

    def test_create_with_priority(self) -> None:
        """TaskCreate should accept a priority level."""
        data = TaskCreate(title="High task", priority=PriorityEnum.HIGH)
        assert data.title == "High task"
        assert data.priority == PriorityEnum.HIGH

    def test_create_with_tags(self) -> None:
        """TaskCreate should accept valid tags."""
        data = TaskCreate(title="Tagged task", tags=["#work", "#urgent"])
        assert data.tags == ["#work", "#urgent"]

    def test_invalid_tag_raises_error(self) -> None:
        """TaskCreate should reject tags without # prefix."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", tags=["invalid"])

    def test_create_with_title_only(self) -> None:
        """TaskCreate should accept a title without description."""
        data = TaskCreate(title="Buy milk")
        assert data.title == "Buy milk"
        assert data.description is None

    def test_create_with_title_and_description(self) -> None:
        """TaskCreate should accept both title and description."""
        data = TaskCreate(title="Buy milk", description="2% from store")
        assert data.title == "Buy milk"
        assert data.description == "2% from store"

    def test_title_is_stripped(self) -> None:
        """TaskCreate should strip whitespace from title."""
        data = TaskCreate(title="  Buy milk  ")
        assert data.title == "Buy milk"

    def test_empty_title_raises_error(self) -> None:
        """TaskCreate should reject empty title."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_whitespace_only_title_raises_error(self) -> None:
        """TaskCreate should reject title with only whitespace."""
        with pytest.raises(ValidationError):
            TaskCreate(title="   ")

    def test_title_too_long_raises_error(self) -> None:
        """TaskCreate should reject title longer than 255 chars."""
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 256)

    def test_description_too_long_raises_error(self) -> None:
        """TaskCreate should reject description longer than 1000 chars."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Valid", description="x" * 1001)


class TestTaskUpdate:
    """Tests for TaskUpdate model validation."""

    def test_update_priority_and_tags(self) -> None:
        """TaskUpdate should accept priority and tags."""
        data = TaskUpdate(priority=PriorityEnum.MEDIUM, tags=["#home"])
        assert data.priority == PriorityEnum.MEDIUM
        assert data.tags == ["#home"]

    def test_invalid_tag_update_raises_error(self) -> None:
        """TaskUpdate should reject invalid tags."""
        with pytest.raises(ValidationError):
            TaskUpdate(tags=["invalid"])

    def test_update_title_only(self) -> None:
        """TaskUpdate should accept title without description."""
        data = TaskUpdate(title="New title")
        assert data.title == "New title"
        assert data.description is None

    def test_update_description_only(self) -> None:
        """TaskUpdate should accept description without title."""
        data = TaskUpdate(description="New description")
        assert data.title is None
        assert data.description == "New description"

    def test_update_both_fields(self) -> None:
        """TaskUpdate should accept both title and description."""
        data = TaskUpdate(title="New title", description="New description")
        assert data.title == "New title"
        assert data.description == "New description"

    def test_empty_update_allowed(self) -> None:
        """TaskUpdate should allow empty initialization (validation at service level)."""
        data = TaskUpdate()
        assert data.title is None
        assert data.description is None

    def test_title_is_stripped(self) -> None:
        """TaskUpdate should strip whitespace from title."""
        data = TaskUpdate(title="  New title  ")
        assert data.title == "New title"

    def test_empty_title_raises_error(self) -> None:
        """TaskUpdate should reject empty title when provided."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="")

    def test_whitespace_title_raises_error(self) -> None:
        """TaskUpdate should reject whitespace-only title when provided."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="   ")


class TestTask:
    """Tests for Task domain model."""

    def test_create_task_with_metadata(self) -> None:
        """Task should store priority and tags."""
        task = Task(id=1, title="Meta task", priority=PriorityEnum.HIGH, tags=["#work"])
        assert task.priority == PriorityEnum.HIGH
        assert task.tags == ["#work"]

    def test_create_task(self) -> None:
        """Task should be created with all required fields."""
        task = Task(id=1, title="Test task")
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description is None
        assert task.completed is False
        assert task.created_at is not None

    def test_task_with_description(self) -> None:
        """Task should accept optional description."""
        task = Task(id=1, title="Test", description="Details")
        assert task.description == "Details"

    def test_task_completed_default_false(self) -> None:
        """Task completed should default to False."""
        task = Task(id=1, title="Test")
        assert task.completed is False

    def test_task_id_must_be_positive(self) -> None:
        """Task should reject non-positive IDs."""
        with pytest.raises(ValidationError):
            Task(id=0, title="Test")

        with pytest.raises(ValidationError):
            Task(id=-1, title="Test")

    def test_task_is_mutable(self) -> None:
        """Task should allow field updates."""
        task = Task(id=1, title="Original")
        task.title = "Updated"
        task.completed = True
        assert task.title == "Updated"
        assert task.completed is True
