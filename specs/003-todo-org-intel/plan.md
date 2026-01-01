# Implementation Plan: Todo Organization & Intelligence

**Branch**: `003-todo-org-intel` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-todo-org-intel/spec.md`

## Summary

Evolve the Todo application with organizational metadata (Priorities, Tags) and intelligence (Due Dates, Recurrence). This implementation focuses on the in-memory core, extending the `Task` model with Pydantic for validation and using `python-dateutil` for robust recurrence calculations. The CLI will be enhanced with filtering, sorting, and overdue highlighting using `Rich`.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: `typer`, `pydantic`, `rich`, `python-dateutil`
**Storage**: In-Memory (Phase I)
**Testing**: `pytest`
**Target Platform**: Linux/WSL (CLI)
**Project Type**: Single project
**Performance Goals**: Instant search/filter (<100ms) for up to 1000 tasks.
**Constraints**: <200ms p95 response time for CLI commands.
**Scale/Scope**: Support for priorities, tagging, and automated recurrence rules.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Decoupled Architecture**: Repository remains isolated; Intelligence Engine resides in Service layer.
- [x] **Type Safety**: Strictly enforced via Pydantic models and Python Enums.
- [x] **Spec-First**: Plan created and artifacts generated before coding.
- [x] **Testable**: Independent test criteria defined in spec.

## Project Structure

### Documentation (this feature)

```text
specs/003-todo-org-intel/
├── spec.md              # Requirements
├── plan.md              # This file
├── research.md          # Research on dateutil and enums
├── data-model.md        # Task and Metadata entities
├── quickstart.md        # CLI usage examples
├── checklists/
│   └── requirements.md  # Spec quality validation
└── contracts/
    └── cli.md           # CLI command contracts
```

### Source Code (repository root)

```text
src/
├── todo/
│   ├── models.py        # Updated with Priority, Tags, Recurrence
│   ├── repository.py    # InMemoryRepository with filter/sort methods
│   ├── service.py       # TaskService with IntelligenceEngine logic
│   ├── ui.py            # Rich-based console output with highlighting
│   └── main.py          # Typer app with new flags (--priority, --tag, etc.)
tests/
├── unit/
│   ├── test_models.py
│   ├── test_recurrence.py
│   └── test_service.py
└── integration/
    └── test_cli_org.py
```

**Structure Decision**: Single project structure extending the existing `src/todo/` package.

## Complexity Tracking

> No violations found.
