"""Shared pytest fixtures for Todo CLI Application tests."""

import pytest
import os
from pathlib import Path

from todo.repository import FileTaskRepository
from todo.service import TaskService


@pytest.fixture
def repository(tmp_path: Path) -> FileTaskRepository:
    """Create a fresh file-based repository for each test using a temp file."""
    test_file = tmp_path / "test_tasks.json"
    return FileTaskRepository(file_path=str(test_file))


@pytest.fixture
def service(repository: FileTaskRepository) -> TaskService:
    """Create a service with the test repository."""
    return TaskService(repository=repository)


@pytest.fixture
def populated_repository(repository: FileTaskRepository) -> FileTaskRepository:
    """Create a repository with sample tasks pre-populated."""
    repository.add("Buy groceries", "Milk, bread, eggs")
    repository.add("Call dentist", "Schedule annual checkup")
    repository.add("Finish report", None)
    return repository


@pytest.fixture
def populated_service(populated_repository: FileTaskRepository) -> TaskService:
    """Create a service with pre-populated data."""
    return TaskService(repository=populated_repository)
