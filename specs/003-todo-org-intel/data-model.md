# Data Model: Todo Organization & Intelligence

## Entities

### Task
Represents a single actionable item with organizational metadata and intelligence rules.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | `int` | Unique identifier (sequential) | Auto-increment |
| `title` | `str` | Task summary | 1-255 chars, non-empty |
| `completed` | `bool` | Completion flag | Default: `False` |
| `priority` | `PriorityEnum` | `HIGH`, `MEDIUM`, `LOW` | Default: `LOW` |
| `tags` | `List[str]` | List of identifiers | Must start with `#` |
| `due_date` | `Optional[datetime]` | Deadlines | ISO 8601, timezone-aware |
| `recurrence` | `RecurrenceEnum` | `DAILY`, `WEEKLY`, `NONE` | Default: `NONE` |
| `created_at` | `datetime` | Creation timestamp | Auto-generated |

### Priority (Enum)
- **HIGH**: Red color coding.
- **MEDIUM**: Yellow color coding.
- **LOW**: Green color coding.

### Recurrence (Enum)
- **DAILY**: Repeats every 24 hours.
- **WEEKLY**: Repeats every 7 days.
- **NONE**: No recurrence.

## Validation Rules

1. **Title**: Must not be empty or whitespace only.
2. **Tags**: Each item in the list must start with exactly one `#` symbol.
3. **Due Date**: Must be a valid date in `YYYY-MM-DD` format when received via CLI strings.
4. **Recurrence**: Required field, defaults to `NONE`.

## State Transitions & Intelligence

### Recurrence Trigger
- **Event**: Task marked as `completed` (transition `False` -> `True`).
- **Condition**: `recurrence` is not `NONE`.
- **Action**:
    1. Calculate `next_due_date` = `max(current_due_date, now) + interval`.
    2. Instantiate duplicate task with `completed=False`, `id=NEW`, `due_date=next_due_date`.
    3. Persist both the completed original and the new instance.
    4. Ensure this only happens once per task (check if original was already completed).
