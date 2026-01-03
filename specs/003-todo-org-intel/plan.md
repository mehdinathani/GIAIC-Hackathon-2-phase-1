# Implementation Plan: Todo Organization & Intelligence

**Branch**: `003-todo-org-intel` | **Date**: 2026-01-01 | **Spec**: [specs/003-todo-org-intel/spec.md](spec.md)
**Input**: Feature specification from `/specs/003-todo-org-intel/spec.md`

## Summary

This feature enhances the Todo application with advanced organization (priority levels, tags, search, filter, sort) and intelligence (due dates, recurring tasks, overdue highlighting). The implementation will leverage the existing Python/Pydantic/Rich stack, utilizing standard library `datetime` for recurrence logic and `rich` for terminal formatting.

## Technical Context

**Language/Version**: Python 3.14
**Primary Dependencies**: Pydantic, Rich, Pytest
**Storage**: JSON file persistence with atomic writes
**Testing**: Pytest (Unit + Integration)
**Target Platform**: CLI (Linux/cross-platform)
**Project Type**: Single project
**Performance Goals**: <2s for filtering 100 tasks, <100ms for search
**Constraints**: <200ms p95, offline-capable
**Scale/Scope**: 100-1000 tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. [X] **Library-First**: Core logic remains in `src/todo/service.py` and `src/todo/models.py`.
2. [X] **CLI Interface**: All features accessible via `todo` commands with standard I/O.
3. [X] **Test-First**: TDD approach for recurrence and filtering units.
4. [X] **Integration Testing**: CLI-level tests for searching and filtering.
5. [X] **Simplicity**: No external database or heavy libraries; standard Python where possible.

## Project Structure

### Documentation (this feature)

```text
specs/003-todo-org-intel/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/todo/
├── models.py       # Updated Pydantic models (Priority, Recurrence)
├── service.py      # Updated logic for recurrence/filtering
├── ui.py           # Updated Rich formatting (colors, bold red)
├── repository.py   # Updated atomic persistence
└── cli.py          # Updated argparse for new commands/flags

tests/
├── unit/
│   ├── test_recurrence.py
│   └── test_service.py
└── integration/
    └── test_cli.py
```

**Structure Decision**: Single project structure as per the existing codebase layout.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |
