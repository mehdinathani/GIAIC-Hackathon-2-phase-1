"""Unit tests for task recurrence logic."""

from datetime import datetime, timedelta
import pytest
from todo.models import TaskCreate, RecurrenceEnum
from todo.service import TaskService
from todo.repository import InMemoryTaskRepository


@pytest.fixture
def service():
    repository = InMemoryTaskRepository()
    return TaskService(repository)


def test_daily_recurrence(service):
    """Completing a DAILY task should create a new task for tomorrow."""
    due_date = datetime(2025, 1, 1, 10, 0, 0)
    task = service.create_task(TaskCreate(
        title="Daily Task",
        due_date=due_date,
        recurrence=RecurrenceEnum.DAILY
    ))

    service.complete_task(task.id)

    tasks = service.list_tasks()
    assert len(tasks) == 2

    new_task = tasks[1]
    assert new_task.title == "Daily Task"
    assert new_task.completed is False
    assert new_task.due_date == due_date + timedelta(days=1)
    assert new_task.recurrence == RecurrenceEnum.DAILY


def test_weekly_recurrence(service):
    """Completing a WEEKLY task should create a new task for next week."""
    due_date = datetime(2025, 1, 1, 10, 0, 0)
    task = service.create_task(TaskCreate(
        title="Weekly Task",
        due_date=due_date,
        recurrence=RecurrenceEnum.WEEKLY
    ))

    service.complete_task(task.id)

    tasks = service.list_tasks()
    assert len(tasks) == 2

    new_task = tasks[1]
    assert new_task.due_date == due_date + timedelta(weeks=1)
    assert new_task.recurrence == RecurrenceEnum.WEEKLY


def test_no_recurrence_by_default(service):
    """Completing a task with RecurrenceEnum.NONE should not create a new task."""
    task = service.create_task(TaskCreate(title="Single Task"))

    service.complete_task(task.id)

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].completed is True
