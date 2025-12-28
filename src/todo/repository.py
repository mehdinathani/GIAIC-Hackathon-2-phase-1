"""Repository layer for Todo CLI Application."""

from typing import Protocol

from todo.models import Task, TaskUpdate


class ITaskRepository(Protocol):
    """Protocol defining the repository interface for task storage."""

    def add(self, title: str, description: str | None = None) -> Task:
        """Create a new task and return it with assigned ID."""
        ...

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by ID, returns None if not found."""
        ...

    def get_all(self) -> list[Task]:
        """Return all tasks ordered by created_at ascending."""
        ...

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        """Update task fields, returns updated task or None if not found."""
        ...

    def delete(self, task_id: int) -> bool:
        """Remove task by ID, returns True if deleted, False if not found."""
        ...

    def exists(self, task_id: int) -> bool:
        """Check if task with ID exists."""
        ...


class InMemoryTaskRepository:
    """In-memory implementation of ITaskRepository using a dictionary."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: str | None = None) -> Task:
        """Create a new task and return it with assigned ID."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by ID, returns None if not found."""
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Return all tasks ordered by created_at ascending."""
        return sorted(self._tasks.values(), key=lambda t: t.created_at)

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        """Update task fields, returns updated task or None if not found."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description

        return task

    def delete(self, task_id: int) -> bool:
        """Remove task by ID, returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def exists(self, task_id: int) -> bool:
        """Check if task with ID exists."""
        return task_id in self._tasks
