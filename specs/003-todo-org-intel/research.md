# Research: Todo Organization & Intelligence

## Decision Log

### Decision: Python `dateutil` for Recurrence Math
- **Rationale**: While Python's `datetime` is sufficient for simple daily recurrence, `python-dateutil` provides robust handling for weekly, monthly, and complex intervals (like "last Friday of the month") which might be needed in future phases. It's the industry standard for RFC 5545 recurrence rules.
- **Alternatives considered**:
  - `datetime` with `timedelta`: Simple, no external dependencies, but harder to maintain for complex patterns.
  - `rrule`: Part of `dateutil`, specifically designed for recurring events.

### Decision: Pydantic Enums for Priority and Recurrence
- **Rationale**: Pydantic's `Enum` support provides strict type validation at the model layer, ensuring invalid strings are rejected before they reach the service or repository.
- **Alternatives considered**:
  - String literals with `Literal`: Good for type checking, but Enums provide better structure for metadata (like colors).

### Decision: Rich for UI Highlighting
- **Rationale**: Already used in the project (per provided plan), `Rich` makes it trivial to apply conditional formatting (bold red for overdue) in the terminal.
- **Alternatives considered**:
  - Manual ANSI codes: Error-prone and harder to read.

## Technical Unknowns & Clarifications

### [RESOLVED] ISO 8601 Date Parsing
- **Decision**: Use `pydantic.validator` or `datetime.fromisoformat()` to ensure strict ISO 8601 compliance for `due_date` inputs from the CLI.

### [RESOLVED] Color Mapping for Priorities
- **Decision**:
  - HIGH: Red
  - MEDIUM: Yellow
  - LOW: Green (or default Dim)
- **Rationale**: Matches common visual cues for urgency.

## Best Practices

- **Separation of Concerns**: The `RecurrenceEngine` should be a standalone utility or service method called by the `TaskService`, keeping the Repository focused only on persistence.
- **Idempotency**: Automatic task creation must be idempotent—marking a task complete multiple times (if somehow possible) should not create duplicate future tasks.
