# Implementation Plan: Interactive CLI Todo App

**Branch**: `002-interactive-cli` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-interactive-cli/spec.md`

## Summary

Enhance the Phase I CLI Todo application with an interactive menu-driven interface using **questionary** for prompts. Users navigate menus with arrow keys, select tasks from lists, and receive visual feedback via chalk-inspired color scheme using Rich panels. Toggle Complete allows both marking and unmarking tasks. This builds on top of Phase I without modifying the existing service/repository layer.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Typer (CLI), Pydantic V2 (Validation), Rich (Formatting/Chalk colors), questionary (Interactive Prompts)
**Storage**: In-memory Python dictionary (unchanged from Phase I)
**Testing**: pytest with fixtures for menu/prompt mocking
**Target Platform**: WSL 2 / Linux / Windows Terminal
**Project Type**: Single project (Console App)
**Performance Goals**: Sub-100ms response time for key presses
**Constraints**: Must run within `uv` environment. Requires terminal with ANSI support. Use chalk-inspired color palette.
**Scale/Scope**: Single user, <1000 tasks

## Constitution Check

*GATE: PASSED*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-First | PASS | Plan created after spec.md approval with clarifications integrated |
| II. Decoupled Architecture | PASS | Reuses Phase I repository pattern, no changes needed |
| III. Type-Safe Python | PASS | Python 3.13+, Pydantic V2, strict type hints |
| IV. Rich CLI | PASS | Rich panels for output with chalk color scheme |
| V. Reusable Intelligence | PASS | Interactive module can be extracted as skill |
| VI. Test-Driven | PASS | pytest tests planned for interactive module |

## Chalk Color Scheme

Per clarification, using chalk-inspired color scheme. Rich supports all standard colors that match the chalk palette:

| Element | Chalk Color | Rich Style |
|---------|-------------|------------|
| Highlight/Selection | Cyan | `cyan` |
| Success | Green | `green` |
| Error | Red | `red` |
| Info | Blue | `blue` |
| Pending | Yellow | `yellow` |
| Muted/Secondary | Gray | `dim` |

Rich Theme configuration:
```python
from rich.theme import Theme
custom_theme = Theme({
    "highlight": "cyan",
    "success": "green",
    "error": "red",
    "info": "blue",
    "pending": "yellow",
    "muted": "dim gray",
})
```

## Project Structure

### Documentation (this feature)

```text
specs/002-interactive-cli/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (complete)
├── research.md          # Phase 0 output (complete)
├── data-model.md        # Phase 1 output (complete)
├── quickstart.md        # Phase 1 output (complete)
├── contracts/           # Phase 1 output (complete)
│   └── interactive-interface.md
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
src/
└── todo/
    ├── __init__.py          # Package init (update for interactive)
    ├── models.py            # Pydantic models (unchanged)
    ├── repository.py        # InMemoryTaskRepository (unchanged)
    ├── service.py           # TaskService (unchanged)
    ├── exceptions.py        # Custom exceptions (unchanged)
    ├── cli.py               # Typer app (add interactive entry point)
    └── interactive.py       # NEW: Interactive menu module

tests/
├── __init__.py
├── conftest.py              # Shared fixtures (add interactive fixtures)
├── unit/
│   ├── __init__.py
│   ├── test_models.py       # (unchanged)
│   ├── test_repository.py   # (unchanged)
│   ├── test_service.py      # (unchanged)
│   └── test_interactive.py  # NEW: Interactive menu unit tests
└── integration/
    ├── __init__.py
    ├── test_cli.py          # (unchanged)
    └── test_interactive_cli.py  # NEW: Interactive CLI integration tests
```

**Structure Decision**: Single project with `src/todo/` package. New `interactive.py` module for menu logic. Reuses existing Phase I structure.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Entry Point (cli.py)                      │
│                                                              │
│    if no subcommand ──► launch_interactive()                │
│    else ──► existing Typer commands                         │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 Interactive Module (interactive.py)          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  MainMenu    │  │  TaskList    │  │  Prompts     │       │
│  │  (select)    │  │  (select)    │  │  (text/conf) │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  Uses: questionary for prompts, Rich for chalk-colored output│
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ uses (unchanged from Phase I)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│                   (service.py - TaskService)                │
│                                                              │
│  • create_task(data: TaskCreate) -> Task                   │
│  • get_task(id: int) -> Task                               │
│  • list_tasks() -> list[Task]                              │
│  • toggle_complete_task(id: int) -> Task                   │
│  • update_task(id: int, data: TaskUpdate) -> Task          │
│  • delete_task(id: int) -> None                            │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ uses
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Repository Layer                           │
│              (repository.py - InMemoryTaskRepository)        │
└─────────────────────────────────────────────────────────────┘
```

## Toggle Complete Logic

Toggle Complete is a bidirectional operation:
- **Pending → Completed**: Sets `task.completed = True`
- **Completed → Pending**: Sets `task.completed = False`

```python
def toggle_complete_task(self, task_id: int) -> Task:
    """Toggle task completion status."""
    task = self._repository.get(task_id)
    if task is None:
        raise TaskNotFoundError(task_id)
    task.completed = not task.completed
    return task
```

## Key Design Decisions

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| questionary library | Built on prompt-toolkit, arrow-key nav built-in | InquirerPy (heavier), raw prompt-toolkit (more work) |
| Rich with chalk colors | Already in project, excellent theming, chalk palette | Colorama (lower-level), termcolor (limited) |
| New interactive.py module | Separation of concerns, easy testing | Embedding in cli.py (too coupled) |
| Toggle Complete | User clarification - can mark and unmark | One-way only (rejected per clarification) |
| No-subcommand entry point | Backward compatible, intuitive UX | New `--interactive` flag (extra typing) |
| Reuse Phase I service layer | Zero code duplication, proven logic | New service for interactive (duplication) |

## Complexity Tracking

No constitution violations to justify.

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research | `specs/002-interactive-cli/research.md` | Complete |
| Data Model | `specs/002-interactive-cli/data-model.md` | Pending (/sp.plan Phase 1) |
| CLI Contract | `specs/002-interactive-cli/contracts/interactive-interface.md` | Pending (/sp.plan Phase 1) |
| Quickstart | `specs/002-interactive-cli/quickstart.md` | Pending (/sp.plan Phase 1) |

## New Dependencies

```bash
uv add questionary
# Rich already in project, Colorama optional for Windows support
```

## NFRs (Non-Functional Requirements)

### Performance
- Menu navigation response: <100ms per key press
- Task list rendering: <200ms for 100 tasks
- Memory footprint: <10MB additional for interactive mode

### Reliability
- Graceful handling of Ctrl+C at any point
- Escape key navigation works from any screen
- Terminal resize doesn't crash the app

### Security
- No external network calls
- Input validation via Pydantic (reuses Phase I)
- No sensitive data exposure in logs

### Accessibility
- High-contrast chalk color scheme for visibility
- Keyboard-only navigation (no mouse required)
- Clear visual feedback for all actions

## Operational Readiness

### Logging
- Rich Console for all output (no syslog needed)
- Errors displayed in red panels

### Error Handling
- TaskNotFoundError wrapped in user-friendly messages
- Empty task list handled gracefully
- Invalid input prompts user to retry

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Terminal doesn't support ANSI | Medium | Check at startup, show warning |
| Questionary compatibility issues | Low | Use prompt-toolkit directly as fallback |
| Windows console issues | Low | Rich handles most cases; Colorama backup |

## Evaluation and Validation

### Definition of Done
- [ ] All 4 user stories implemented
- [ ] Toggle Complete works bidirectionally
- [ ] Chalk color scheme applied to all UI
- [ ] All 92 existing tests still pass
- [ ] New interactive tests added
- [ ] Ruff linting passes
- [ ] Manual quickstart testing complete

## Next Steps

Run `/sp.tasks` to generate atomic, testable implementation tasks from this plan.
