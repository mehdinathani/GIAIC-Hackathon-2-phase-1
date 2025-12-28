"""Unit tests for TaskService business logic."""

import pytest

from todo.exceptions import TaskNotFoundError
from todo.models import TaskCreate, TaskUpdate
from todo.service import TaskService


class TestCreateTask:
    """Tests for create task service operation."""

    def test_create_task_returns_task(self, service: TaskService) -> None:
        """Create should return the created task."""
        data = TaskCreate(title="New task")
        task = service.create_task(data)
        assert task.id == 1
        assert task.title == "New task"
        assert task.completed is False

    def test_create_task_with_description(self, service: TaskService) -> None:
        """Create should accept description."""
        data = TaskCreate(title="New task", description="Details here")
        task = service.create_task(data)
        assert task.description == "Details here"

    def test_create_multiple_tasks(self, service: TaskService) -> None:
        """Create should assign sequential IDs."""
        task1 = service.create_task(TaskCreate(title="Task 1"))
        task2 = service.create_task(TaskCreate(title="Task 2"))
        assert task1.id == 1
        assert task2.id == 2


class TestGetTask:
    """Tests for get task service operation."""

    def test_get_existing_task(self, populated_service: TaskService) -> None:
        """Get should return existing task."""
        task = populated_service.get_task(1)
        assert task.id == 1
        assert task.title == "Buy groceries"

    def test_get_nonexistent_raises_error(self, service: TaskService) -> None:
        """Get should raise TaskNotFoundError for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.get_task(999)
        assert exc_info.value.task_id == 999

    def test_error_message_contains_id(self, service: TaskService) -> None:
        """TaskNotFoundError should contain the task ID in message."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.get_task(42)
        assert "42" in str(exc_info.value)


class TestListTasks:
    """Tests for list tasks service operation."""

    def test_list_empty(self, service: TaskService) -> None:
        """List should return empty list when no tasks."""
        tasks = service.list_tasks()
        assert tasks == []

    def test_list_all_tasks(self, populated_service: TaskService) -> None:
        """List should return all tasks."""
        tasks = populated_service.list_tasks()
        assert len(tasks) == 3

    def test_list_preserves_order(self, populated_service: TaskService) -> None:
        """List should return tasks in creation order."""
        tasks = populated_service.list_tasks()
        titles = [t.title for t in tasks]
        assert titles == ["Buy groceries", "Call dentist", "Finish report"]


class TestCompleteTask:
    """Tests for complete task service operation (mark as complete)."""

    def test_complete_existing_task(self, populated_service: TaskService) -> None:
        """Complete should mark task as completed."""
        task = populated_service.complete_task(1)
        assert task.completed is True

    def test_complete_returns_updated_task(self, populated_service: TaskService) -> None:
        """Complete should return the updated task."""
        task = populated_service.complete_task(1)
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.completed is True

    def test_complete_nonexistent_raises_error(self, service: TaskService) -> None:
        """Complete should raise TaskNotFoundError for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.complete_task(999)
        assert exc_info.value.task_id == 999

    def test_complete_already_completed(self, populated_service: TaskService) -> None:
        """Complete should succeed even if already completed."""
        populated_service.complete_task(1)
        task = populated_service.complete_task(1)
        assert task.completed is True


class TestUpdateTask:
    """Tests for update task service operation."""

    def test_update_title(self, populated_service: TaskService) -> None:
        """Update should change task title."""
        data = TaskUpdate(title="Updated groceries")
        task = populated_service.update_task(1, data)
        assert task.title == "Updated groceries"

    def test_update_description(self, populated_service: TaskService) -> None:
        """Update should change task description."""
        data = TaskUpdate(description="Updated description")
        task = populated_service.update_task(1, data)
        assert task.description == "Updated description"

    def test_update_both_fields(self, populated_service: TaskService) -> None:
        """Update should change both title and description."""
        data = TaskUpdate(title="New title", description="New desc")
        task = populated_service.update_task(1, data)
        assert task.title == "New title"
        assert task.description == "New desc"

    def test_update_nonexistent_raises_error(self, service: TaskService) -> None:
        """Update should raise TaskNotFoundError for non-existent ID."""
        data = TaskUpdate(title="New title")
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.update_task(999, data)
        assert exc_info.value.task_id == 999

    def test_update_preserves_completion_status(
        self, populated_service: TaskService
    ) -> None:
        """Update should not affect completion status."""
        populated_service.complete_task(1)
        data = TaskUpdate(title="New title")
        task = populated_service.update_task(1, data)
        assert task.completed is True


class TestDeleteTask:
    """Tests for delete task service operation."""

    def test_delete_existing_task(self, populated_service: TaskService) -> None:
        """Delete should succeed for existing task."""
        populated_service.delete_task(1)
        # Verify deletion by checking list
        tasks = populated_service.list_tasks()
        assert len(tasks) == 2
        assert all(t.id != 1 for t in tasks)

    def test_delete_returns_none(self, populated_service: TaskService) -> None:
        """Delete should return None (no value)."""
        result = populated_service.delete_task(1)
        assert result is None

    def test_delete_nonexistent_raises_error(self, service: TaskService) -> None:
        """Delete should raise TaskNotFoundError for non-existent ID."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.delete_task(999)
        assert exc_info.value.task_id == 999

    def test_delete_twice_raises_error(self, populated_service: TaskService) -> None:
        """Delete should raise error when deleting same task twice."""
        populated_service.delete_task(1)
        with pytest.raises(TaskNotFoundError):
            populated_service.delete_task(1)


class TestIntegration:
    """Integration tests for combined service operations."""

    def test_full_task_lifecycle(self, service: TaskService) -> None:
        """Test complete task lifecycle: create, update, complete, delete."""
        # Create
        task = service.create_task(TaskCreate(title="Test task"))
        assert task.id == 1

        # Update
        updated = service.update_task(1, TaskUpdate(description="Added description"))
        assert updated.description == "Added description"

        # Complete
        completed = service.complete_task(1)
        assert completed.completed is True

        # List
        tasks = service.list_tasks()
        assert len(tasks) == 1

        # Delete
        service.delete_task(1)
        tasks = service.list_tasks()
        assert len(tasks) == 0

    def test_multiple_tasks_operations(self, service: TaskService) -> None:
        """Test operations on multiple tasks."""
        # Create 3 tasks
        t1 = service.create_task(TaskCreate(title="Task 1"))
        t2 = service.create_task(TaskCreate(title="Task 2"))
        t3 = service.create_task(TaskCreate(title="Task 3"))

        # Complete one
        service.complete_task(t2.id)

        # Update another
        service.update_task(t1.id, TaskUpdate(title="Updated Task 1"))

        # Delete one
        service.delete_task(t3.id)

        # Verify state
        tasks = service.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Updated Task 1"
        assert tasks[0].completed is False
        assert tasks[1].title == "Task 2"
        assert tasks[1].completed is True
