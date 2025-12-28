"""Unit tests for InMemoryTaskRepository."""

import pytest

from todo.models import TaskUpdate
from todo.repository import InMemoryTaskRepository


class TestAdd:
    """Tests for add task functionality."""

    def test_add_task_returns_task_with_id(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Add should return task with assigned ID."""
        task = repository.add("Buy milk")
        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description is None
        assert task.completed is False

    def test_add_task_with_description(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Add should accept optional description."""
        task = repository.add("Buy milk", "2% from store")
        assert task.description == "2% from store"

    def test_add_increments_id(self, repository: InMemoryTaskRepository) -> None:
        """Each added task should get sequential ID."""
        task1 = repository.add("Task 1")
        task2 = repository.add("Task 2")
        task3 = repository.add("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_stores_task(self, repository: InMemoryTaskRepository) -> None:
        """Added task should be retrievable."""
        task = repository.add("Test task")
        retrieved = repository.get(task.id)
        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.title == task.title


class TestGet:
    """Tests for get task functionality."""

    def test_get_existing_task(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Get should return existing task."""
        task = populated_repository.get(1)
        assert task is not None
        assert task.id == 1
        assert task.title == "Buy groceries"

    def test_get_nonexistent_task_returns_none(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Get should return None for non-existent ID."""
        result = repository.get(999)
        assert result is None

    def test_get_after_delete_returns_none(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Get should return None after task is deleted."""
        populated_repository.delete(1)
        result = populated_repository.get(1)
        assert result is None


class TestGetAll:
    """Tests for list all tasks functionality."""

    def test_get_all_empty_repository(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Get all should return empty list for empty repository."""
        tasks = repository.get_all()
        assert tasks == []

    def test_get_all_returns_all_tasks(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Get all should return all tasks."""
        tasks = populated_repository.get_all()
        assert len(tasks) == 3

    def test_get_all_ordered_by_created_at(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Get all should return tasks ordered by creation time."""
        tasks = populated_repository.get_all()
        for i in range(len(tasks) - 1):
            assert tasks[i].created_at <= tasks[i + 1].created_at


class TestUpdate:
    """Tests for update task functionality."""

    def test_update_title(self, populated_repository: InMemoryTaskRepository) -> None:
        """Update should change task title."""
        update_data = TaskUpdate(title="Updated title")
        task = populated_repository.update(1, update_data)
        assert task is not None
        assert task.title == "Updated title"

    def test_update_description(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Update should change task description."""
        update_data = TaskUpdate(description="Updated description")
        task = populated_repository.update(1, update_data)
        assert task is not None
        assert task.description == "Updated description"

    def test_update_both_fields(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Update should change both title and description."""
        update_data = TaskUpdate(title="New title", description="New desc")
        task = populated_repository.update(1, update_data)
        assert task is not None
        assert task.title == "New title"
        assert task.description == "New desc"

    def test_update_nonexistent_returns_none(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Update should return None for non-existent task."""
        update_data = TaskUpdate(title="New title")
        result = repository.update(999, update_data)
        assert result is None

    def test_update_preserves_other_fields(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Update should not affect fields not being updated."""
        original = populated_repository.get(1)
        assert original is not None
        original_created = original.created_at
        original_completed = original.completed

        update_data = TaskUpdate(title="New title")
        task = populated_repository.update(1, update_data)
        assert task is not None
        assert task.created_at == original_created
        assert task.completed == original_completed


class TestDelete:
    """Tests for delete task functionality."""

    def test_delete_existing_task(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Delete should return True for existing task."""
        result = populated_repository.delete(1)
        assert result is True

    def test_delete_removes_task(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Delete should remove task from repository."""
        populated_repository.delete(1)
        assert populated_repository.get(1) is None
        assert len(populated_repository.get_all()) == 2

    def test_delete_nonexistent_returns_false(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Delete should return False for non-existent task."""
        result = repository.delete(999)
        assert result is False

    def test_delete_twice_returns_false(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Delete should return False when deleting same task twice."""
        populated_repository.delete(1)
        result = populated_repository.delete(1)
        assert result is False


class TestExists:
    """Tests for exists check functionality."""

    def test_exists_returns_true_for_existing(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Exists should return True for existing task."""
        assert populated_repository.exists(1) is True
        assert populated_repository.exists(2) is True
        assert populated_repository.exists(3) is True

    def test_exists_returns_false_for_nonexistent(
        self, repository: InMemoryTaskRepository
    ) -> None:
        """Exists should return False for non-existent task."""
        assert repository.exists(1) is False
        assert repository.exists(999) is False

    def test_exists_after_delete(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Exists should return False after task is deleted."""
        assert populated_repository.exists(1) is True
        populated_repository.delete(1)
        assert populated_repository.exists(1) is False


class TestMarkComplete:
    """Tests for marking tasks as complete (via direct mutation)."""

    def test_mark_task_complete(
        self, populated_repository: InMemoryTaskRepository
    ) -> None:
        """Task should be markable as complete via direct mutation."""
        task = populated_repository.get(1)
        assert task is not None
        assert task.completed is False

        task.completed = True

        # Verify the change persists
        retrieved = populated_repository.get(1)
        assert retrieved is not None
        assert retrieved.completed is True
