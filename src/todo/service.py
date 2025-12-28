"""Service layer for Todo CLI Application."""

from todo.exceptions import TaskNotFoundError
from todo.models import Task, TaskCreate, TaskUpdate
from todo.repository import ITaskRepository


class TaskService:
    """Business logic layer for task operations."""

    def __init__(self, repository: ITaskRepository) -> None:
        self._repository = repository

    def create_task(self, data: TaskCreate) -> Task:
        """Create a new task from validated input data."""
        return self._repository.add(
            title=data.title,
            description=data.description,
        )

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by ID, raises TaskNotFoundError if not found."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def list_tasks(self) -> list[Task]:
        """Return all tasks from repository."""
        return self._repository.get_all()

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed, raises TaskNotFoundError if not found."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        task.completed = True
        return task

    def toggle_complete_task(self, task_id: int) -> Task:
        """Toggle task completion status bidirectionally.

        If task is pending, mark as complete. If task is complete, mark as pending.
        Raises TaskNotFoundError if task not found.
        """
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        task.completed = not task.completed
        return task

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        """Update task fields, raises TaskNotFoundError if not found."""
        task = self._repository.update(task_id, data)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task, raises TaskNotFoundError if not found."""
        if not self._repository.delete(task_id):
            raise TaskNotFoundError(task_id)
