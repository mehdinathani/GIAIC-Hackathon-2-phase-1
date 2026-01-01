# Todo Evolution: Phase II

An evolved Todo CLI application with organizational metadata and intelligence features.

## Features

- **Organization**: Assign Priorities (HIGH, MEDIUM, LOW) and multiple Tags to tasks.
- **Intelligence**: Set Due Dates and define Recurrence rules (DAILY, WEEKLY).
- **Search & Filter**: Filter tasks by priority, tags, or search keywords in titles and descriptions.
- **Rich UI**: Color-coded priority levels, tag highlighting, and overdue alerts in bold red.
- **Interactive Mode**: Launch a TUI by running `todo` without arguments.

## Installation

```bash
uv sync
```

## Quick Start

### Add a task with metadata
```bash
todo add "Finish report" --priority HIGH --tag #work --due 2026-01-02
```

### List tasks with filters
```bash
todo list --filter-priority HIGH --sort due
```

### Search tasks
```bash
todo list --search "report"
```

### Complete a recurring task
```bash
todo complete 1
# If recurrence was DAILY, a new task will be spawned for tomorrow.
```

## Development

Run tests with:
```bash
uv run pytest
```

Validate recurrence matching with the specialized skill:
```bash
uv run python .specify/skills/validate-recurrence.py
```
