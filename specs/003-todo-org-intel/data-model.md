# Data Model: Todo Organization & Intelligence

## Entities

### Task
Represents a single actionable item with organizational metadata and intelligence rules.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | `UUID` | Unique identifier | Auto-generated |
| `title` | `str` | Task description | Non-empty |
| `status` | `StatusEnum` | `INCOMPLETE` or `COMPLETE` | Default: `INCOMPLETE` |
| `priority` | `PriorityEnum` | `HIGH`, `MEDIUM`, `LOW` | Default: `LOW` |
| `tags` | `List[str]` | List of `#hashtags` | Must start with `#` |
| `due_date` | `Optional[datetime]` | When the task is due | ISO 8601 format |
| `recurrence` | `Optional[RecurrenceEnum]` | `DAILY`, `WEEKLY`, `NONE` | Default: `NONE` |

### Priority (Enum)
- **HIGH**: Critical/Urgent (Red)
- **MEDIUM**: Standard/Important (Yellow)
- **LOW**: Minor/Routine (Green/White)

### Recurrence (Enum)
- **DAILY**: Repeats every day.
- **WEEKLY**: Repeats every 7 days.

## State Transitions

### Completion Flow
1. User marks `Task` as `COMPLETE`.
2. System checks `Task.recurrence`.
3. If `DAILY` or `WEEKLY`:
   - System calculates `next_due_date` based on current `due_date` (or today if null).
   - System creates a NEW `Task` instance with `status=INCOMPLETE`.
   - New `Task` inherits `title`, `priority`, `tags`, and `recurrence` from parent.
