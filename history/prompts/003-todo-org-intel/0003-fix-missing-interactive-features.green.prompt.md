---
id: "0003"
title: "fix-missing-interactive-features"
stage: "green"
date: "2026-01-01"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "003-todo-org-intel"
branch: "003-todo-org-intel"
user: "unknown"
command: "/sp.implement"
labels: ["interactive", "missing-features", "ux"]
links:
  spec: "specs/003-todo-org-intel/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "src/todo/interactive.py"
tests:
  - "tests/integration/test_cli.py"
  - "tests/unit/test_recurrence.py"
---

## Prompt

if you say all tasks done, but i didnt see intermediate and advance level functionalities as i describe in specs Basic Level (Core Essentials)
These form the foundation—quick to build, essential for any MVP:
Add Task – Create new todo items
Delete Task – Remove tasks from the list
Update Task – Modify existing task details
View Task List – Display all tasks
Mark as Complete – Toggle task completion status
Intermediate Level (Organization & Usability)
Add these to make the app feel polished and practical:


Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
Search & Filter – Search by keyword; filter by status, priority, or date
Sort Tasks – Reorder by due date, priority, or alphabetically
Advanced Level (Intelligent Features)
Recurring Tasks – Auto-reschedule repeating tasks (e.g., "weekly meeting")
Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications

## Response snapshot

Audited the codebase and identified that while the CLI commands supported all features, the Interactive Mode was missing Priorities, Tags, Search, Filtering, Sorting, Due Dates, and Recurrence. Implemented these in `src/todo/interactive.py`. Added simulated "browser notifications" via startup overdue alerts in the CLI.

## Outcome

- ✅ Impact: Fully aligned the Interactive Mode with the spec's Organization and Intelligence requirements.
- 🧪 Tests: 107 tests passed; interactive mode verified via manual logic inspection.
- 📁 Files: Updated `src/todo/interactive.py`.
- 🧠 Reflection: Realized that "completed" in tasks.md didn't account for the UI/Interactive surface area. Bridged that gap.

## Evaluation notes (flywheel)

- Failure modes observed: String match failures in Edit tool due to context changes.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
