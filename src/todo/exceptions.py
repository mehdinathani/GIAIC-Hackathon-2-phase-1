"""Custom exceptions for Todo CLI Application."""


class TaskNotFoundError(Exception):
    """Raised when a task with the specified ID is not found."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")
