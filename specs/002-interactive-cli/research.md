# Research: Phase II - Interactive CLI

**Branch**: `002-interactive-cli` | **Date**: 2025-12-28

## Research Summary

All technical decisions align with the Constitution and enhance the Phase I foundation.

---

## Decision 1: Interactive Prompt Library

**Decision**: questionary

**Rationale**:
- Pure Python library built on prompt-toolkit
- Provides select, text, confirm, and checkbox prompts out-of-the-box
- Arrow-key navigation built-in for select prompts
- Custom styling support via Style objects
- Graceful keyboard interrupt handling (returns None on Ctrl+C)
- Async support via ask_async() for future extensibility
- High source reputation, 34+ code snippets available
- Lightweight with minimal dependencies

**Alternatives Considered**:
- InquirerPy: More features but heavier, PyInquirer-compatible syntax
- prompt-toolkit: Lower-level, requires more boilerplate for simple menus
- PyInquirer: Older, less maintained than questionary

---

## Decision 2: Visual Styling

**Decision**: Rich library (already in Phase I) + questionary Style

**Rationale**:
- Constitution mandates Rich for CLI output (Principle IV)
- questionary provides its own Style class for prompt customization
- Consistent color scheme: green (success), red (error), blue (info), cyan (highlight)
- Can combine Rich panels for messages with questionary for interactive prompts

**Implementation**:
- Use Rich for static output (success messages, task details, headers)
- Use questionary Style for interactive prompt highlighting
- Define shared color constants for consistency

---

## Decision 3: Application Entry Point

**Decision**: New interactive mode command alongside existing CLI

**Rationale**:
- Preserve existing `uv run todo add/list/complete/update/delete` commands
- Add new `uv run todo` (no subcommand) to launch interactive mode
- Allows both quick CLI usage and full interactive experience
- Non-breaking change for Phase I functionality

**Implementation**:
- If `todo` called without subcommand, launch interactive menu
- If subcommand provided, use existing Phase I behavior
- Use Typer callback for default behavior detection

---

## Decision 4: Screen Management

**Decision**: Console clear + redraw pattern

**Rationale**:
- Standard approach for terminal menu applications
- questionary handles input capture in raw mode
- Rich console.clear() for screen transitions
- No external curses/ncurses dependency needed

**Implementation**:
- Clear screen when entering new menu/view
- Redraw header + menu options
- Return to previous screen on Escape/Back

---

## Decision 5: State Management

**Decision**: Reuse Phase I repository/service pattern

**Rationale**:
- Constitution requires decoupled Service-Repository architecture (Principle II)
- Phase I already has InMemoryTaskRepository and TaskService
- Interactive CLI is just a new presentation layer
- Zero changes needed to business logic

**Implementation**:
- Import existing TaskService from todo.service
- Import existing repository from todo.repository
- Add new interactive.py module for menu logic

---

## Decision 6: Module Structure

**Decision**: Single new module `interactive.py`

**Rationale**:
- Keep interactive logic separate from existing cli.py
- Single responsibility: menu navigation and prompt handling
- Imports from existing models, service, repository
- Easy to test independently

**Structure**:
- `src/todo/interactive.py`: Menu class, prompt handlers, main loop
- Integration in `src/todo/cli.py`: Typer callback for no-subcommand case

---

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Interactive library | questionary (prompt-toolkit based) |
| Styling approach | Rich + questionary Style combo |
| Entry point | `todo` without subcommand |
| Screen management | Clear + redraw pattern |
| State management | Reuse Phase I service/repository |
| Module structure | New interactive.py module |

---

## Dependencies to Add

- questionary: Interactive prompts with arrow-key navigation

---

## Next Steps

Proceed to Phase 1: Design data model and CLI contracts.
