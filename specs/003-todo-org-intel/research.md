# Research: Todo Organization & Intelligence

## Decision Log

### Decision: Python Standard Library for Date Math
- **Rationale**: The requirements specifically call for DAILY and WEEKLY recurrence. Python's `datetime` and `timedelta` handle these intervals flawlessly including leap years and month transitions. No external library is needed for these simple intervals.
- **Alternatives considered**:
  - `python-dateutil`: Industry standard for rrules, but overkill for just DAILY/WEEKLY.
  - `pendulum`: Excellent API but adds a heavy dependency for simple math.

### Decision: Pydantic Enums for Priority and Recurrence
- **Rationale**: Pydantic's `Enum` support provides strict type validation at the model layer, ensuring invalid strings are rejected before they reach the service or repository.
- **Alternatives considered**:
  - String literals with `Literal`: Good for type checking, but Enums provide better structure for metadata (like colors).

### Decision: Rich for UI Highlighting
- **Rationale**: `Rich` is already an implicit dependency for modern CLI apps and makes it trivial to apply conditional formatting (bold red for overdue) and tables in the terminal.
- **Alternatives considered**:
  - Manual ANSI codes: Error-prone and harder to read.

### Decision: Storage Strategy
- **Decision**: Continue using JSON file persistence with atomic writes (temporary file + rename).
- **Rationale**: Current scale (100-1000 tasks) doesn't justify SQLite overhead. Atomic writes prevent corruption on save failures.

## Technical Unknowns & Clarifications

### [RESOLVED] ISO 8601 Date Parsing
- **Decision**: Use `pydantic.field_validator` to enforce `datetime.fromisoformat()` and ensure strict ISO 8601 compliance for `due_date`.

### [RESOLVED] Color Mapping for Priorities
- **Decision**:
  - HIGH: [bold red]
  - MEDIUM: [yellow]
  - LOW: [green]
- **Rationale**: Standard hazard/urgency colors.

### [RESOLVED] Search Implementation
- **Decision**: Case-insensitive substring matching in title and tags using list comprehensions.
- **Rationale**: Extremely fast for <10,000 items in memory.

## Best Practices

- **Separation of Concerns**: Recurrence logic lives in a `TaskEngine` or service layer, NOT the repository.
- **Atomic Persistence**: Always use `os.replace` (or equivalent) for atomic writes.
- **Idempotency**: Ensure that marking a task complete only triggers recurrence once to avoid duplicates.
