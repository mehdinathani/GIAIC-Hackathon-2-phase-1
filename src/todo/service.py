"""Service layer for Todo CLI Application."""

from datetime import datetime
from todo.exceptions import TaskNotFoundError
from todo.models import PriorityEnum, RecurrenceEnum, Task, TaskCreate, TaskUpdate
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
            priority=data.priority,
            tags=data.tags,
            due_date=data.due_date,
            recurrence=data.recurrence,
        )

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by ID, raises TaskNotFoundError if not found."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def list_tasks(
        self,
        filter_priority: PriorityEnum | None = None,
        filter_tag: str | None = None,
        search_query: str | None = None,
        sort_by: str | None = None,
    ) -> list[Task]:
        """Return all tasks from repository with optional filtering and sorting."""
        return self._repository.get_all(
            filter_priority=filter_priority,
            filter_tag=filter_tag,
            search_query=search_query,
            sort_by=sort_by,
        )

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed, handle recurrence if applicable."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        if not task.completed:
            task.completed = True

            # Handle recurrence
            if task.recurrence != RecurrenceEnum.NONE:
                next_due = self._calculate_next_due(task.due_date, task.recurrence)
                new_task_data = TaskCreate(
                    title=task.title,
                    description=task.description,
                    priority=task.priority,
                    tags=task.tags,
                    due_date=next_due,
                    recurrence=task.recurrence,
                )
                self.create_task(new_task_data)

        return task

    def toggle_complete_task(self, task_id: int) -> Task:
        """Toggle task completion status bidirectionally.

        If task is pending, mark as complete. If task is complete, mark as pending.
        Raises TaskNotFoundError if task not found.
        """
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        if not task.completed:
            return self.complete_task(task_id)
        else:
            task.completed = False
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

    def is_overdue(self, task: Task) -> bool:
        """Check if a task is overdue (not completed and past due date)."""
        if task.completed or task.due_date is None:
            return False
        return task.due_date < datetime.now()

    def _calculate_next_due(
        self, current_due: datetime | None, recurrence: RecurrenceEnum
    ) -> datetime:
        """Calculate next due date based on recurrence rule."""
        from datetime import timedelta

        base_date = current_due or datetime.now()
        if recurrence == RecurrenceEnum.DAILY:
            return base_date + timedelta(days=1)
        if recurrence == RecurrenceEnum.WEEKLY:
            return base_date + timedelta(weeks=1)
        return base_date
