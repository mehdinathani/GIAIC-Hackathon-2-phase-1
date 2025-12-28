# Tasks: Phase II - Interactive CLI

**Input**: Design documents from `/specs/002-interactive-cli/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/interactive-interface.md

**Tests**: Not explicitly requested in specification. Tests omitted per task generation rules.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[USx]**: Which user story this task belongs to (US1, US2, US3, US4)
- Paths use `src/todo/` package structure per plan.md

---

## Phase 1: Setup

**Purpose**: Install new dependency and prepare module structure

- [x] T001 Add questionary dependency with `uv add questionary`
- [x] T002 Create `src/todo/interactive.py` with module docstring and imports
- [x] T003 [P] Create MenuAction enum in `src/todo/interactive.py` per data-model.md (UPDATE to TOGGLE_COMPLETE)
- [x] T004 [P] Create TaskAction enum in `src/todo/interactive.py` per data-model.md
- [x] T005 [P] Create custom questionary Style in `src/todo/interactive.py` per data-model.md ColorScheme

**Checkpoint**: New dependency installed, interactive module scaffolded with enums and styles.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core interactive infrastructure required by ALL user stories

**CRITICAL**: No user story implementation can begin until this phase is complete.

- [x] T006 Create `InteractiveApp` class skeleton in `src/todo/interactive.py` with service injection
- [x] T007 Create `clear_screen()` utility function in `src/todo/interactive.py`
- [x] T008 Create `print_header(title: str)` utility function in `src/todo/interactive.py` using Rich
- [x] T009 Create `print_success(message: str)` utility function in `src/todo/interactive.py` using Rich Panel
- [x] T010 Create `print_error(message: str)` utility function in `src/todo/interactive.py` using Rich Panel
- [x] T011 Create `print_info(message: str)` utility function in `src/todo/interactive.py` using Rich Panel
- [x] T012 Create `wait_for_enter()` utility function in `src/todo/interactive.py`
- [x] T013 Add Typer callback to `src/todo/cli.py` to detect no-subcommand invocation
- [x] T014 Create `launch_interactive()` function in `src/todo/cli.py` to start interactive mode

**Checkpoint**: Foundation ready - utility functions, app class, and entry point established.

---

## Phase 3: User Story 1 - Interactive Main Menu Navigation (Priority: P1)

**Goal**: Display main menu with 5 options and handle arrow-key navigation.

**Independent Test**: Run `uv run todo` and verify menu appears with navigation working.

### Implementation for User Story 1

- [x] T015 [US1] Create `_get_menu_choices()` method in InteractiveApp returning list of menu options
- [x] T016 [US1] Create `show_main_menu()` method in InteractiveApp using questionary.select
- [x] T017 [US1] Implement menu header display in `show_main_menu()` using Rich
- [x] T018 [US1] Create `run()` main loop method in InteractiveApp with menu dispatch logic
- [x] T019 [US1] Implement Exit option handler with goodbye message in `src/todo/interactive.py`
- [x] T020 [US1] Implement graceful Ctrl+C / Escape handling in `run()` loop
- [x] T021 [US1] Wire up InteractiveApp instantiation in `launch_interactive()` in `src/todo/cli.py`

**Checkpoint**: MVP Complete. Users can launch app, see menu, navigate, and exit.

---

## Phase 4: User Story 2 - Interactive Task List Selection (Priority: P2)

**Goal**: Display tasks in selectable list with visual highlighting.

**Independent Test**: Add tasks via Phase I CLI, then run `uv run todo` and select View List.

### Implementation for User Story 2

- [x] T022 [US2] Create `_format_task_choice(task: Task)` helper method in InteractiveApp
- [x] T023 [US2] Create `show_task_list()` method in InteractiveApp using questionary.select
- [x] T024 [US2] Implement empty list handling with "No tasks found" info panel and add option
- [x] T025 [US2] Create `show_task_actions(task: Task)` method displaying context menu
- [x] T026 [US2] Wire View Task List menu option to `show_task_list()` in `run()` dispatch

**Checkpoint**: Task list selection complete. Users can view and select tasks.

---

## Phase 5: User Story 3 - Inline Task Creation with Prompts (Priority: P3)

**Goal**: Add tasks through guided title and description prompts.

**Independent Test**: Run `uv run todo`, select Add Task, follow prompts, verify task created.

### Implementation for User Story 3

- [x] T027 [US3] Create `prompt_task_title()` method in InteractiveApp using questionary.text
- [x] T028 [US3] Create `prompt_task_description()` method in InteractiveApp using questionary.text
- [x] T029 [US3] Create `handle_add_task()` method orchestrating title/description prompts
- [x] T030 [US3] Implement Escape cancellation handling in `handle_add_task()`
- [x] T031 [US3] Display success panel with task details after creation
- [x] T032 [US3] Wire Add Task menu option to `handle_add_task()` in `run()` dispatch

**Checkpoint**: Task creation complete. Users can add tasks through prompts.

---

## Phase 6: User Story 4 - Quick Actions from Task List (Priority: P4)

**Goal**: Perform complete/update/delete actions directly from task context menu.

**Independent Test**: View task list, select a task, perform each action type.

### Implementation for User Story 4

- [x] T033 [US4] Create `handle_toggle_complete(task: Task)` method in InteractiveApp (toggle bidirectionally)
- [x] T034 [US4] Create `handle_update_task(task: Task)` method with title/description prompts
- [x] T035 [US4] Create `handle_delete_task(task: Task)` method with confirmation prompt
- [x] T036 [US4] Implement delete confirmation using questionary.confirm with default=False
- [x] T037 [US4] Wire task action handlers to `show_task_actions()` dispatch logic
- [x] T038 [US4] Wire Toggle Complete main menu option to task selection + toggle flow
- [x] T039 [US4] Wire Update Task main menu option to task selection + update flow
- [x] T040 [US4] Wire Delete Task main menu option to task selection + delete flow

**Checkpoint**: All CRUD operations complete via interactive mode.

---

## Phase 7: Polish and Quality Assurance

**Purpose**: Error handling, edge cases, and code quality

- [x] T041 Add keyboard interrupt handler (Ctrl+C) for graceful exit throughout app
- [x] T042 [P] Add docstrings to all public methods in `src/todo/interactive.py`
- [x] T043 [P] Add type hints to all methods in `src/todo/interactive.py`
- [x] T044 Run `uv run ruff check src/ --fix` and `uv run ruff format src/`
- [x] T045 Verify all menu options work per `specs/002-interactive-cli/quickstart.md`
- [x] T046 Test edge case: empty task list flow
- [x] T047 Test edge case: Escape key cancellation at all prompts

**Checkpoint**: Production-ready interactive CLI with documentation and linting.

---

## Bonus: TAB Toggle Feature

**Purpose**: Quick task completion toggle from task list (per clarification 2025-12-28)

- [x] T048 Add prompt_toolkit Keys and KeyBindings imports for advanced key handling
- [x] T049 Create `_format_task_for_display()` helper for status-indicated task formatting
- [x] T050 Create `_show_task_list_with_tab_toggle()` using prompt-toolkit Application with custom key bindings
- [x] T051 Implement TAB key handler to toggle task completion with visual feedback
- [x] T052 Display color change and "(now COMPLETE/PENDING)" indicator after toggle

**Checkpoint**: TAB toggle working with visual feedback. User stays on same task.

---

## Dependencies and Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ─────────────────────────────────────────────┐
                                                              │
Phase 2 (Foundational) ◄──────────────────────────────────────┘
        │
        ├─────► Phase 3 (US1: Main Menu) ─► MVP Complete!
        │
        ├─────► Phase 4 (US2: Task List) ◄── requires US1
        │
        ├─────► Phase 5 (US3: Add Task) ◄── can parallel with US2
        │
        └─────► Phase 6 (US4: Quick Actions) ◄── requires US2
                        │
                        ▼
              Phase 7 (Polish)

BONUS: TAB Toggle ◄── enhances US2 task list experience
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|---------------------|
| US1 (P1) | Phase 2 only | None (MVP first) |
| US2 (P2) | Phase 2 + US1 main loop | US3 after US1 done |
| US3 (P3) | Phase 2 + US1 main loop | US2 after US1 done |
| US4 (P4) | Phase 2 + US1 + US2 task list | None |
| TAB Toggle | US2 task list | Can be added anytime |

### Parallel Opportunities Within Phases

**Phase 1**: T003, T004, T005 can run in parallel
**Phase 2**: T007, T008, T009, T010, T011, T012 can run in parallel (utility functions)
**Phase 7**: T042, T043 can run in parallel
**Bonus**: T048-T052 can run in parallel (different methods)

---

## Implementation Strategy

### MVP First (Recommended)

1. **Complete Phase 1**: Setup (T001-T005)
2. **Complete Phase 2**: Foundation (T006-T014)
3. **Complete Phase 3**: User Story 1 (T015-T021)
4. **STOP and VALIDATE**: Test menu navigation with `uv run todo`
5. Deploy/demo MVP if ready

### Full Implementation

1. Complete Phases 1-3 (MVP)
2. Add Phase 4: User Story 2 (T022-T026)
3. Add Phase 5: User Story 3 (T027-T032)
4. Add Phase 6: User Story 4 (T033-T040)
5. Complete Phase 7: Polish (T041-T047)
6. Final validation against quickstart.md

### Bonus: TAB Toggle

- Add T048-T052 for quick task completion from list view
- Provides efficient workflow enhancement
- Visual feedback confirms toggle action

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Setup | T001-T005 (5) | Dependency and module scaffolding |
| Foundation | T006-T014 (9) | Core infrastructure, entry point |
| US1 (P1) | T015-T021 (7) | Main menu navigation |
| US2 (P2) | T022-T026 (5) | Task list selection |
| US3 (P3) | T027-T032 (6) | Add task prompts |
| US4 (P4) | T033-T040 (8) | Quick actions |
| Polish | T041-T047 (7) | Quality assurance |
| Bonus | T048-T052 (5) | TAB toggle with visual feedback |
| **Total** | **52 tasks** | |

---

## Notes

- [P] tasks = different files/functions, safe to parallelize
- [USx] label maps task to user story for traceability
- All file paths are relative to repository root
- Phase I code (models, repository, service) is unchanged
- New code goes in `src/todo/interactive.py` and entry point in `src/todo/cli.py`
- Toggle Complete replaces Mark Complete per clarification
- Chalk color scheme implemented via Rich Theme configuration
- TAB Toggle feature added per clarification 2025-12-28 for efficient task completion
