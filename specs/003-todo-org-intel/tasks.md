# Tasks: Todo Organization & Intelligence

**Input**: Design documents from `/specs/003-todo-org-intel/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [X] T001 Verify `pydantic` and `rich` are installed and up to date in `pyproject.toml`
- [X] T002 [P] Create initial documentation files in `specs/003-todo-org-intel/` (completed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core model updates and utilities that all user stories depend on

- [X] T003 [P] Implement `PriorityEnum` and `RecurrenceEnum` in `src/todo/models.py`
- [X] T004 Update `Task` and `TaskCreate`/`TaskUpdate` models with `priority`, `tags`, `due_date`, and `recurrence` in `src/todo/models.py`
- [X] T005 [P] Implement atomic write helper for repository persistence in `src/todo/repository.py`
- [X] T006 Add unit tests for new model fields and validation in `tests/unit/test_models.py`

**Checkpoint**: Core models ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Task Organization (Priority: P1) 🎯 MVP

**Goal**: Support priority levels and multi-tagging for tasks

**Independent Test**: Create a task with HIGH priority and #work tags, then verify they display with colors in the list.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Define priority color mapping using Rich styles in `src/todo/ui.py`
- [ ] T008 [US1] Update `add` and `update` logic for `--priority` and `--tags` in `src/todo/service.py`
- [ ] T009 [US1] Update Command Line Interface to accept `--priority` and `--tags` in `src/todo/cli.py`
- [ ] T010 [US1] Update task list rendering to display color-coded priority and tags in `src/todo/ui.py`
- [ ] T011 [US1] Add unit tests for priority and tag propagation in `tests/unit/test_service.py`

**Checkpoint**: Priority and tagging are fully functional and testable

---

## Phase 4: User Story 2 - Search, Filter, and Sort (Priority: P1)

**Goal**: Implement keyword search and filtering/sorting by metadata

**Independent Test**: Use `todo list --search milk` or `todo list --filter-priority HIGH` and verify results.

### Implementation for User Story 2

- [ ] T012 [US2] Implement `search` and `filter` logic in `TaskService` in `src/todo/service.py`
- [ ] T013 [US2] Implement `sort` logic (priority Desc, due_date Asc) in `TaskService` in `src/todo/service.py`
- [ ] T014 [US2] Add `--search`, `--filter-priority`, `--filter-status`, and `--sort` flags to `list` command in `src/todo/cli.py`
- [ ] T015 [US2] Handle "No tasks found" feedback for search/filter in `src/todo/ui.py`
- [ ] T016 [US2] Add integration tests for search/filter/sort CLI commands in `tests/integration/test_cli.py`

**Checkpoint**: Users can efficiently find and organize their workload

---

## Phase 5: User Story 3 - Due Dates and Reminders (Priority: P2)

**Goal**: Support deadline tracking and overdue alerts

**Independent Test**: Set a due date in the past and see the task listed in BOLD RED.

### Implementation for User Story 3

- [ ] T017 [US3] Update `add` and `update` commands for `--due-date` flag in `src/todo/cli.py`
- [ ] T018 [US3] Implement overdue detection logic in `src/todo/service.py`
- [ ] T019 [US3] Apply [bold red] formatting to overdue task titles in `src/todo/ui.py`
- [ ] T020 [US3] Add unit tests for overdue calculation logic in `tests/unit/test_service.py`

**Checkpoint**: Due dates and visual reminders are functional

---

## Phase 6: User Story 4 - Recurring Tasks (Priority: P3)

**Goal**: Automated creation of routine tasks upon completion

**Independent Test**: Complete a "DAILY" task and see a new instance for tomorrow appear in the list.

### Implementation for User Story 4

- [ ] T021 [US4] Update `add` command for `--recurrence` flag (DAILY, WEEKLY) in `src/todo/cli.py`
- [ ] T022 [US4] Implement recurrence instance generation logic in `src/todo/service.py`
- [ ] T023 [US4] Trigger recurrence engine during `complete_task` flow in `src/todo/service.py`
- [ ] T024 [US4] Add unit tests for lease year and month-end recurrence math in `tests/unit/test_recurrence.py`

**Checkpoint**: Recurring tasks are being automatically spawned correctly

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, error handling, and documentation

- [ ] T025 [P] Implement interactive re-prompting for invalid inputs in `src/todo/cli.py`
- [ ] T026 Implement persistence failure (Retry/Save As) error handling in `src/todo/repository.py`
- [ ] T027 Run all scenarios from `specs/003-todo-org-intel/quickstart.md`
- [ ] T028 [P] Update project `CLAUDE.md` and `README.md` with new features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 2 (Foundational)**: MUST be completed before any User Story phases because all feature logic depends on the updated model schema and repository helpers.
- **User Stories (Phase 3-6)**: Are mostly independent after Phase 2, but US4 benefits from US3 (due dates).
- **Phase 7 (Polish)**: Final hardening and cleanup.

### Parallel Opportunities

- **T003 & T005**: Models and repository helpers can be modified in parallel.
- **T007**: UI Styles can be defined while service logic is being worked on.
- **T006, T011, T016, T020, T024**: Unit and integration tests can be written alongside implementation.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Start with **Phase 2** (Models/Repository).
2. Complete **US1** (Priorities/Tags) to provide immediate visual value.
3. Complete **US2** (Search/Filter/Sort) to handle growing task lists.
4. **VALDIATE**: Ensure core organization is robust before adding intelligence.

### Intelligence Layer

1. Add **US3** (Due Dates) to introduce the temporal dimension.
2. Finish with **US4** (Recurrence) and **Phase 7** for a complete automated experience.
