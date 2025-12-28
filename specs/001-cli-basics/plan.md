# Implementation Plan: Phase I - CLI Basics

**Branch**: `001-cli-basics` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification for an in-memory Python console app using Typer and Pydantic.

## Summary

Build a modular CLI todo application implementing a **Service-Repository pattern**:
1. **Repository Layer**: Handles data storage abstraction (In-memory dict for Phase I)
2. **Service Layer**: Handles business logic and validation
3. **CLI Layer**: Handles user interface via Typer/Rich

This architecture ensures Phase II migration to PostgreSQL requires **zero changes** to Service logic.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Typer (CLI), Pydantic V2 (Validation), Rich (Formatting)
**Storage**: In-memory Python dictionary keyed by task ID
**Testing**: pytest with fixtures for repository mocking
**Target Platform**: WSL 2 / Linux
**Project Type**: Single project (Console App)
**Performance Goals**: Sub-100ms response time for all CLI commands
**Constraints**: Must run within `uv` environment. Memory cleared on process exit.
**Scale/Scope**: Single user, <1000 tasks

## Constitution Check

*GATE: PASSED*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-First | PASS | Plan created after spec.md approval |
| II. Decoupled Architecture | PASS | Repository pattern with ITaskRepository protocol |
| III. Type-Safe Python | PASS | Python 3.13+, Pydantic V2, strict type hints |
| IV. Rich CLI | PASS | All output via Rich tables/panels |
| V. Reusable Intelligence | PASS | Repository pattern enables skill reuse |
| VI. Test-Driven | PASS | pytest tests planned for all layers |

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-basics/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (complete)
├── research.md          # Phase 0 output (complete)
├── data-model.md        # Phase 1 output (complete)
├── quickstart.md        # Phase 1 output (complete)
├── contracts/           # Phase 1 output (complete)
│   └── cli-interface.md # CLI command contracts
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Phase 2 output (next: /sp.tasks)
```

### Source Code (repository root)

```text
src/
└── todo/
    ├── __init__.py          # Package init, version
    ├── models.py            # Task, TaskCreate, TaskUpdate (Pydantic)
    ├── repository.py        # ITaskRepository protocol + InMemoryTaskRepository
    ├── service.py           # TaskService (business logic)
    ├── exceptions.py        # TaskNotFoundError, custom exceptions
    └── cli.py               # Typer app with all commands

tests/
├── __init__.py
├── conftest.py              # Shared fixtures (repository, service)
├── unit/
│   ├── __init__.py
│   ├── test_models.py       # Model validation tests
│   ├── test_repository.py   # Repository CRUD tests
│   └── test_service.py      # Service logic tests
└── integration/
    ├── __init__.py
    └── test_cli.py          # CLI command integration tests
```

**Structure Decision**: Single project with `src/todo/` package. Tests mirror source structure.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                            │
│                      (cli.py - Typer)                       │
│  ┌─────┐ ┌──────┐ ┌──────────┐ ┌────────┐ ┌────────┐       │
│  │ add │ │ list │ │ complete │ │ update │ │ delete │       │
│  └──┬──┘ └──┬───┘ └────┬─────┘ └───┬────┘ └───┬────┘       │
└─────┼───────┼──────────┼───────────┼──────────┼────────────┘
      │       │          │           │          │
      └───────┴──────────┴─────┬─────┴──────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                           │
│                   (service.py - TaskService)                │
│                                                             │
│  • create_task(data: TaskCreate) -> Task                   │
│  • get_task(id: int) -> Task                               │
│  • list_tasks() -> list[Task]                              │
│  • complete_task(id: int) -> Task                          │
│  • update_task(id: int, data: TaskUpdate) -> Task          │
│  • delete_task(id: int) -> None                            │
└─────────────────────────────────────────────────────────────┘
                               │
                               │ uses
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Repository Layer                          │
│              (repository.py - ITaskRepository)              │
│                                                             │
│  Protocol:                                                  │
│  • add(task: Task) -> Task                                 │
│  • get(id: int) -> Task | None                             │
│  • get_all() -> list[Task]                                 │
│  • update(id: int, data: TaskUpdate) -> Task | None        │
│  • delete(id: int) -> bool                                 │
│  • exists(id: int) -> bool                                 │
└─────────────────────────────────────────────────────────────┘
                               △
                               │ implements
                               │
┌─────────────────────────────────────────────────────────────┐
│              InMemoryTaskRepository (Phase I)               │
│                                                             │
│  _tasks: dict[int, Task]                                   │
│  _next_id: int = 1                                         │
└─────────────────────────────────────────────────────────────┘
```

## Dependency Injection

```python
# Application wiring (in cli.py or __init__.py)
repository = InMemoryTaskRepository()
service = TaskService(repository=repository)
app = create_cli(service=service)
```

Phase II change: Only replace repository instantiation:
```python
repository = PostgresTaskRepository(connection_string)  # New
service = TaskService(repository=repository)            # Unchanged
app = create_cli(service=service)                       # Unchanged
```

## Key Design Decisions

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| Repository Protocol | Enables storage swap without service changes | Direct dict access (tight coupling) |
| Pydantic DTOs | Clear input validation, separate from domain model | Dict/tuple passing (no validation) |
| Rich output | Professional CLI UX per constitution | Plain print (poor UX) |
| Sequential IDs | User-friendly CLI references | UUID (hard to type) |
| pytest fixtures | Clean test isolation, repository mocking | Manual setup/teardown |

## Complexity Tracking

No constitution violations to justify.

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research | `specs/001-cli-basics/research.md` | Complete |
| Data Model | `specs/001-cli-basics/data-model.md` | Complete |
| CLI Contract | `specs/001-cli-basics/contracts/cli-interface.md` | Complete |
| Quickstart | `specs/001-cli-basics/quickstart.md` | Complete |

## Next Steps

Run `/sp.tasks` to generate atomic, testable implementation tasks from this plan.
