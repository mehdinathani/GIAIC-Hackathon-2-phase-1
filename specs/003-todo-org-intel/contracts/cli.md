# Contracts: Task Organization & Intelligence (CLI)

The CLI interface is the primary contract for this Phase.

## Commands

### `add`
Adds a new task with optional organization metadata.

**Arguments:**
- `title` (string, required)

**Flags:**
- `--priority`, `-p`: [high|medium|low] (default: low)
- `--tag`, `-t`: One or more tags (e.g., `-t work -t personal`)
- `--due`, `-d`: ISO date string (YYYY-MM-DD)
- `--recur`, `-r`: [daily|weekly]

---

### `list`
Lists tasks with sorting and filtering capabilities.

**Flags:**
- `--filter-priority`: Show only tasks with specific priority.
- `--filter-tag`: Show only tasks with specific tag.
- `--sort`: [priority|due] (default: id/created)
- `--status`: [complete|incomplete|all] (default: incomplete)

---

### `update`
Modifies an existing task's metadata.

**Arguments:**
- `task_id` (UUID, required)

**Flags:**
- `--priority`: Update priority.
- `--tag`: Replace or add tags.
- `--due`: Update due date.
- `--recur`: Update recurrence pattern.

---

### `complete`
Marks a task as complete and triggers intelligence engine for recurrence.

**Arguments:**
- `task_id` (UUID, required)

**Behavior:**
- Updates status to `COMPLETE`.
- If `recurrence` is set, prints: `New recurring instance created for [DATE]`.
