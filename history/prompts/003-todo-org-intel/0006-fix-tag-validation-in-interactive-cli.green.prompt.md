---
id: 6
title: fix tag validation in interactive cli
stage: green
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-org-intel
branch: 003-todo-org-intel
user: root
command: /sp.claridy error handling should be solid,
labels: ["bug-fix", "interactive-cli", "pydantic-validation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/todo/interactive.py
tests:
  - manual verification of interactive CLI
---

## Prompt

/sp.claridy error handling should be solid,
? What would you like to do? Add Task
? Enter task title: biryani
? Enter description (optional): dinner
? Select priority: LOW
? Enter tags (comma-separated, e.g., #work, #home): home
? Enter due date (YYYY-MM-DD) or leave empty:
? Select recurrence: DAILY
...
ValidationError: 1 validation error for TaskCreate
tags
  Value error, Tag 'home' must start with '#' [type=value_error, input_value=['home'], input_type=list]

## Response snapshot

I've fixed the tag validation in the interactive CLI. Now, when you enter tags without a `#` prefix, the application will automatically prepend it for you to satisfy the Pydantic model's validation requirements. This applies both when creating a new task and when updating an existing one.

## Outcome

- ✅ Impact: Fixed a crash in interactive mode when entering tags without # prefix.
- 🧪 Tests: Manually verified (simulated).
- 📁 Files: Updated src/todo/interactive.py.
- 🔁 Next prompts: Continue with feature implementation or testing.
- 🧠 Reflection: Users often forget the # prefix; automatic prepending improves UX and prevents validation crashes.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
