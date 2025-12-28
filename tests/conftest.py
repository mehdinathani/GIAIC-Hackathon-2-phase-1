"""Shared pytest fixtures for Todo CLI Application tests."""

import pytest

from todo.repository import InMemoryTaskRepository
from todo.service import TaskService


@pytest.fixture
def repository() -> InMemoryTaskRepository:
    """Create a fresh in-memory repository for each test."""
    return InMemoryTaskRepository()


@pytest.fixture
def service(repository: InMemoryTaskRepository) -> TaskService:
    """Create a service with the test repository."""
    return TaskService(repository=repository)


@pytest.fixture
def populated_repository(repository: InMemoryTaskRepository) -> InMemoryTaskRepository:
    """Create a repository with sample tasks pre-populated."""
    repository.add("Buy groceries", "Milk, bread, eggs")
    repository.add("Call dentist", "Schedule annual checkup")
    repository.add("Finish report", None)
    return repository


@pytest.fixture
def populated_service(populated_repository: InMemoryTaskRepository) -> TaskService:
    """Create a service with pre-populated data."""
    return TaskService(repository=populated_repository)
