"""Repository layer for Todo CLI Application."""

import json
import os
from datetime import datetime
from typing import Protocol, cast
from pathlib import Path

from todo.models import PriorityEnum, RecurrenceEnum, Task, TaskUpdate


class ITaskRepository(Protocol):
    """Protocol defining the repository interface for task storage."""

    def add(
        self,
        title: str,
        description: str | None = None,
        priority: PriorityEnum = PriorityEnum.LOW,
        tags: list[str] = None,
        due_date: datetime | None = None,
        recurrence: RecurrenceEnum = RecurrenceEnum.NONE,
    ) -> Task:
        """Create a new task and return it with assigned ID."""
        ...

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by ID, returns None if not found."""
        ...

    def get_all(
        self,
        filter_priority: PriorityEnum | None = None,
        filter_tag: str | None = None,
        filter_status: bool | None = None,
        search_query: str | None = None,
        sort_by: str | None = None,
    ) -> list[Task]:
        """Return all tasks with optional filtering and sorting."""
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


class FileTaskRepository:
    """JSON file implementation of ITaskRepository with atomic writes."""

    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = Path(file_path)
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load tasks from JSON file."""
        if not self.file_path.exists():
            self._tasks = {}
            self._next_id = 1
            return

        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self._tasks = {
                    int(k): Task.model_validate(v) for k, v in data.items()
                }
                if self._tasks:
                    self._next_id = max(self._tasks.keys()) + 1
                else:
                    self._next_id = 1
        except (json.JSONDecodeError, IOError):
            self._tasks = {}
            self._next_id = 1

    def _save(self) -> None:
        """Save tasks to JSON file using atomic write (write + rename)."""
        temp_path = self.file_path.with_suffix(".tmp")
        try:
            with open(temp_path, "w") as f:
                # Use model_dump for Pydantic serialization
                data = {
                    str(k): v.model_dump(mode="json")
                    for k, v in self._tasks.items()
                }
                json.dump(data, f, indent=2)

            # Atomic swap
            os.replace(temp_path, self.file_path)
        except IOError as e:
            if temp_path.exists():
                temp_path.unlink()
            raise RuntimeError(f"Failed to save tasks: {e}")

    def add(
        self,
        title: str,
        description: str | None = None,
        priority: PriorityEnum = PriorityEnum.LOW,
        tags: list[str] = None,
        due_date: datetime | None = None,
        recurrence: RecurrenceEnum = RecurrenceEnum.NONE,
    ) -> Task:
        """Create a new task and return it with assigned ID."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence=recurrence,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        self._save()
        return task

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by ID, returns None if not found."""
        return self._tasks.get(task_id)

    def get_all(
        self,
        filter_priority: PriorityEnum | None = None,
        filter_tag: str | None = None,
        filter_status: bool | None = None,
        search_query: str | None = None,
        sort_by: str | None = None,
    ) -> list[Task]:
        """Return all tasks with optional filtering and sorting."""
        tasks = list(self._tasks.values())

        # Filtering
        if filter_priority:
            tasks = [t for t in tasks if t.priority == filter_priority]
        if filter_tag:
            tasks = [t for t in tasks if filter_tag in t.tags]
        if filter_status is not None:
            tasks = [t for t in tasks if t.completed == filter_status]
        if search_query:
            query = search_query.lower()
            tasks = [
                t for t in tasks
                if query in t.title.lower() or (t.description and query in t.description.lower())
            ]

        # Sorting
        if sort_by == "priority":
            # High (0), Medium (1), Low (2)
            priority_map = {PriorityEnum.HIGH: 0, PriorityEnum.MEDIUM: 1, PriorityEnum.LOW: 2}
            tasks.sort(key=lambda t: (priority_map[t.priority], t.created_at))
        elif sort_by == "due":
            # Tasks without due date go to the end
            tasks.sort(key=lambda t: (t.due_date is None, t.due_date, t.created_at))
        elif sort_by == "title":
            tasks.sort(key=lambda t: (t.title.lower(), t.created_at))
        else:
            # Default sort by created_at ascending
            tasks.sort(key=lambda t: t.created_at)

        return tasks

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        """Update task fields, returns updated task or None if not found."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.completed is not None:
            task.completed = data.completed
        if data.priority is not None:
            task.priority = data.priority
        if data.tags is not None:
            task.tags = data.tags
        if data.due_date is not None:
            task.due_date = data.due_date
        if data.recurrence is not None:
            task.recurrence = data.recurrence

        self._save()
        return task

    def delete(self, task_id: int) -> bool:
        """Remove task by ID, returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()
            return True
        return False

    def exists(self, task_id: int) -> bool:
        """Check if task with ID exists."""
        return task_id in self._tasks


# maintain fallback name for existing CLI imports if necessary
InMemoryTaskRepository = FileTaskRepository
