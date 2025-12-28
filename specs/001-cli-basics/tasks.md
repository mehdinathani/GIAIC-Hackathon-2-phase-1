# Tasks: Phase I - CLI Basics

**Input**: Design documents from `/specs/001-cli-basics/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-interface.md

**Tests**: Not explicitly requested in specification. Tests omitted per task generation rules.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Paths use `src/todo/` package structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management

- [x] T001 Create project structure with `src/todo/` and `tests/` directories
- [x] T002 [P] Add `__init__.py` files to `src/todo/`, `tests/`, `tests/unit/`, `tests/integration/`
- [x] T003 [P] Install core dependencies: `uv add typer pydantic rich`
- [x] T004 [P] Install dev dependencies: `uv add --dev pytest ruff`
- [x] T005 Configure `pyproject.toml` with ruff settings and `[project.scripts]` entry point

**Checkpoint**: Project initialized with all dependencies installed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models, repository interface, and service layer required by ALL user stories

**CRITICAL**: No CLI command implementation can begin until this phase is complete.

- [x] T006 [P] Create `TaskNotFoundError` exception in `src/todo/exceptions.py`
- [x] T007 [P] Create Pydantic models (Task, TaskCreate, TaskUpdate) in `src/todo/models.py` per data-model.md
- [x] T008 Create `ITaskRepository` protocol and `InMemoryTaskRepository` in `src/todo/repository.py`
- [x] T009 Create `TaskService` class skeleton in `src/todo/service.py` with repository injection
- [x] T010 Create base Typer app in `src/todo/cli.py` with app instance and Rich console
- [x] T011 Wire up dependency injection in `src/todo/__init__.py` (repository -> service -> app)

**Checkpoint**: Foundation ready - 3-layer architecture established, ready for CLI commands.

---

## Phase 3: User Story 1 - Core Task Creation and Visibility (Priority: P1)

**Goal**: Enable users to add tasks and see them in a formatted table.

**Independent Test**: Run `uv run todo add "Buy Milk"` then `uv run todo list`.

### Implementation for User Story 1

- [x] T012 [US1] Implement `add()` method in `InMemoryTaskRepository` in `src/todo/repository.py`
- [x] T013 [US1] Implement `get_all()` method in `InMemoryTaskRepository` in `src/todo/repository.py`
- [x] T014 [US1] Implement `create_task()` method in `TaskService` in `src/todo/service.py`
- [x] T015 [US1] Implement `list_tasks()` method in `TaskService` in `src/todo/service.py`
- [x] T016 [US1] Create `add` command with `@app.command()` in `src/todo/cli.py`
- [x] T017 [US1] Create `list` command with `@app.command()` in `src/todo/cli.py`
- [x] T018 [US1] Implement Rich Table output for `list` command in `src/todo/cli.py`
- [x] T019 [US1] Implement Rich Panel success output for `add` command in `src/todo/cli.py`
- [x] T020 [US1] Handle empty list state with "No tasks found" info panel

**Checkpoint**: MVP Complete. Users can add tasks and view them in a formatted table.

---

## Phase 4: User Story 2 - Task Completion and Removal (Priority: P2)

**Goal**: Allow users to mark tasks complete and delete them.

**Independent Test**: Run `uv run todo complete 1` and verify status. Run `uv run todo delete 1` and verify removal.

### Implementation for User Story 2

- [x] T021 [US2] Implement `get()` method in `InMemoryTaskRepository` in `src/todo/repository.py`
- [x] T022 [US2] Implement `delete()` method in `InMemoryTaskRepository` in `src/todo/repository.py`
- [x] T023 [US2] Implement `complete_task()` method in `TaskService` in `src/todo/service.py`
- [x] T024 [US2] Implement `delete_task()` method in `TaskService` in `src/todo/service.py`
- [x] T025 [US2] Create `complete` command with `@app.command()` in `src/todo/cli.py`
- [x] T026 [US2] Create `delete` command with `@app.command()` in `src/todo/cli.py`
- [x] T027 [US2] Add TaskNotFoundError handling with Rich error panel in `src/todo/cli.py`

**Checkpoint**: Lifecycle management complete. Users can complete and delete tasks.

---

## Phase 5: User Story 3 - Task Detail Modification (Priority: P3)

**Goal**: Allow users to update task title and description.

**Independent Test**: Run `uv run todo update 1 --title "New Title"` and verify change.

### Implementation for User Story 3

- [x] T028 [US3] Implement `update()` method in `InMemoryTaskRepository` in `src/todo/repository.py`
- [x] T029 [US3] Implement `update_task()` method in `TaskService` in `src/todo/service.py`
- [x] T030 [US3] Create `update` command with optional `--title` and `--description` flags in `src/todo/cli.py`
- [x] T031 [US3] Add validation to require at least one field for update in `src/todo/cli.py`

**Checkpoint**: All CRUD operations complete. Full feature set available.

---

## Phase 6: Polish & Quality Assurance

**Purpose**: Error handling, documentation, and code quality

- [x] T032 Add global exception handler for TaskNotFoundError in `src/todo/cli.py`
- [x] T033 [P] Add docstrings to all public methods in `src/todo/service.py`
- [x] T034 [P] Add docstrings to all public methods in `src/todo/repository.py`
- [x] T035 [P] Add command help descriptions to all CLI commands in `src/todo/cli.py`
- [x] T036 Run `uv run ruff check src/ --fix` and `uv run ruff format src/`
- [x] T037 Verify all commands work per `specs/001-cli-basics/quickstart.md`

**Checkpoint**: Production-ready code with documentation and linting.

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ─────────────────────────────────────────────┐
                                                              │
Phase 2 (Foundational) ◄──────────────────────────────────────┘
        │
        ├─────► Phase 3 (US1: Add/List) ─► MVP Complete!
        │
        ├─────► Phase 4 (US2: Complete/Delete)
        │
        └─────► Phase 5 (US3: Update)
                        │
                        ▼
              Phase 6 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US1 (P1) | Phase 2 only | None (MVP first) |
| US2 (P2) | Phase 2 + US1 `get()` | US3 after US1 done |
| US3 (P3) | Phase 2 + US1 `get()` | US2 after US1 done |

### Parallel Opportunities Within Phases

**Phase 1**: T002, T003, T004 can run in parallel
**Phase 2**: T006, T007 can run in parallel
**Phase 6**: T033, T034, T035 can run in parallel

---

## Parallel Example: Phase 2 Foundation

```bash
# These tasks can run in parallel (different files):
Task: "T006 Create TaskNotFoundError in src/todo/exceptions.py"
Task: "T007 Create Pydantic models in src/todo/models.py"

# Then sequentially:
Task: "T008 Create repository in src/todo/repository.py" (needs T007)
Task: "T009 Create service in src/todo/service.py" (needs T008)
```

---

## Implementation Strategy

### MVP First (Recommended)

1. **Complete Phase 1**: Setup (T001-T005)
2. **Complete Phase 2**: Foundation (T006-T011)
3. **Complete Phase 3**: User Story 1 (T012-T020)
4. **STOP and VALIDATE**: Test `add` and `list` commands
5. Deploy/demo MVP if ready

### Full Implementation

1. Complete Phases 1-3 (MVP)
2. Add Phase 4: User Story 2 (T021-T027)
3. Add Phase 5: User Story 3 (T028-T031)
4. Complete Phase 6: Polish (T032-T037)
5. Final validation against quickstart.md

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Setup | T001-T005 (5) | Project initialization |
| Foundation | T006-T011 (6) | Models, Repository, Service, CLI base |
| US1 (P1) | T012-T020 (9) | Add + List commands |
| US2 (P2) | T021-T027 (7) | Complete + Delete commands |
| US3 (P3) | T028-T031 (4) | Update command |
| Polish | T032-T037 (6) | Documentation, linting, validation |
| **Total** | **37 tasks** | |

---

## Notes

- [P] tasks = different files, safe to parallelize
- [USx] label maps task to user story for traceability
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- All file paths are relative to repository root
