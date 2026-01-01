# Tasks: Todo Organization & Intelligence

**Input**: Design documents from `/specs/003-todo-org-intel/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [X] T001 Install `python-dateutil` and update project dependencies
- [X] T002 [P] Create initial documentation files in `specs/003-todo-org-intel/` (completed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core model updates that all user stories depend on

- [X] T003 Update `Task` model with `PriorityEnum` and `Tags` in `src/todo/models.py`
- [X] T004 Add `due_date` and `recurrence` fields to `Task` model in `src/todo/models.py`
- [X] T005 [P] Implement `PriorityEnum` and `RecurrenceEnum` in `src/todo/models.py`

**Checkpoint**: Core models ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Task Organization (Priority: P1) 🎯 MVP

**Goal**: Support priority levels and multi-tagging for tasks

**Independent Test**: Create a task with HIGH priority and #work tags, then verify they display with colors in the list.

### Implementation for User Story 1

- [X] T006 [P] [US1] Implement priority color mapping in `src/todo/ui.py`
- [X] T007 [US1] Update `add` command in `src/todo/main.py` for `--priority` and `--tag`
- [X] T008 [US1] Update `update` command in `src/todo/main.py` for `--priority` and `--tag`
- [X] T009 [US1] Update task list rendering to show priority and tags in `src/todo/ui.py`
- [X] T010 [US1] Add unit tests for priority and tag storage in `tests/unit/test_models.py`

**Checkpoint**: Priority and tagging are fully functional and testable

---

## Phase 4: User Story 2 - Search, Filter, and Sort (Priority: P1)

**Goal**: Implement keyword search and filtering/sorting by metadata

**Independent Test**: Use `todo list --filter-priority high` or `todo list --sort due` and verify results.

### Implementation for User Story 2

- [X] T011 [US2] Add filter/search methods to `InMemoryRepository` in `src/todo/repository.py`
- [X] T012 [US2] Add sort logic to `InMemoryRepository` in `src/todo/repository.py`
- [X] T013 [US2] Integrate search/filter/sort into `TaskService` in `src/todo/service.py`
- [X] T014 [US2] Add `--filter-priority`, `--filter-tag`, and `--sort` flags to `list` command in `src/todo/main.py`
- [X] T015 [US2] Add unit tests for search and filter logic in `tests/unit/test_service.py`

**Checkpoint**: Users can search, filter, and sort their tasks effectively

---

## Phase 5: User Story 3 - Due Dates and Reminders (Priority: P2)

**Goal**: Support deadline tracking and overdue alerts

**Independent Test**: Set a due date in the past and see the task listed in BOLD RED.

### Implementation for User Story 3

- [X] T016 [US3] Update `add` and `update` commands for `--due` flag in `src/todo/cli.py`
- [X] T017 [US3] Implement overdue detection logic in `src/todo/service.py`
- [X] T018 [US3] Add conditional BOLD RED formatting for overdue tasks in `src/todo/ui.py`
- [X] T019 [US3] Add unit tests for overdue calculation in `tests/unit/test_service.py`

**Checkpoint**: Due dates and reminders are functional

---

## Phase 6: User Story 4 - Recurring Tasks (Priority: P3)

**Goal**: Automated creation of routine tasks upon completion

**Independent Test**: Complete a "DAILY" task and see a new instance for tomorrow appear in the list.

### Implementation for User Story 4

- [X] T020 [US4] Update `add` command for `--recur` flag in `src/todo/cli.py`
- [X] T021 [US4] Implement `RecurrenceEngine` logic in `src/todo/service.py`
- [X] T022 [US4] Integrate recurrence engine into the `complete` command flow in `src/todo/service.py`
- [X] T023 [US4] Add unit tests for DAILY and WEEKLY recurrence math in `tests/unit/test_recurrence.py`
- [X] T024 [P] [US4] Build a Claude Code **Skill** for validating task recurrence logic in `.specify/skills/validate-recurrence.py`

**Checkpoint**: Recurring tasks are being automatically spawned correctly

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [X] T025 Run `quickstart.md` validation scenarios
- [X] T026 Perform final CLI help text cleanup in `src/todo/cli.py`
- [X] T027 [P] Update project README with new organization and intelligence features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Install `python-dateutil` first.
- **Foundational (Phase 2)**: Mandatory for all user stories.
- **User Stories (Phase 3-6)**: Can proceed in parallel after Phase 2.
- **Polish (Phase 7)**: Requires all user stories to be complete.

### User Story Dependencies

- **US1 & US2**: High Priority - MVP focus.
- **US3**: Depends on `due_date` field (Foundation).
- **US4**: Depends on `recurrence` field (Foundation) and utilizes `TaskService` (Foundation).

## Parallel Opportunities

- **T005**: Models can be defined while other foundational work is planned.
- **US1 & US2**: Can be implemented simultaneously if state doesn't conflict.
- **T010, T015, T019, T023**: All unit test tasks can run in parallel with their implementations.
- **T024**: Skill creation can happen in parallel with recurrence engine implementation.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Phase 1 & 2.
2. Complete US1 (Priorities/Tags).
3. Complete US2 (Search/Filter/Sort).
4. **STOP and VALDIATE**: Ensure core organization is robust.

### Incremental Delivery

1. Add US3 (Due Dates) to enable deadline tracking.
2. Add US4 (Recurrence) to complete the intelligence suite.
3. Validate each increment with the provided `quickstart.md` scenarios.
