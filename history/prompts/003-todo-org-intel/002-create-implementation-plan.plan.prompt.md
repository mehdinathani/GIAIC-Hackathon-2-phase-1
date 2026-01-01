---
id: 2
title: Implementation Plan for Todo Organization & Intelligence
stage: plan
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-todo-org-intel
branch: 003-todo-org-intel
user: local-user
command: /sp.plan
labels: [plan, architecture, design, research]
links:
  spec: specs/003-todo-org-intel/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-todo-org-intel/plan.md
  - specs/003-todo-org-intel/research.md
  - specs/003-todo-org-intel/data-model.md
  - specs/003-todo-org-intel/contracts/cli.md
  - specs/003-todo-org-intel/quickstart.md
tests:
  - null
---

## Prompt

# Implementation Plan: Todo Organization & Intelligence (Phase I)

**Feature**: `003-todo-org-intel` | **Phase**: I (In-Memory)
**Scope**: Intermediate (Priorities, Tags) & Advanced (Recurrence, Due Dates)

## Summary
Evolve the existing in-memory CLI to support metadata (Priorities/Tags) and automated logic (Recurrence). We will use Python Enums for strict typing and the `datetime` module for date calculations.

## Technical Context
- **Language**: Python 3.13
- **Libraries**: `typer`, `pydantic`, `rich`, `python-dateutil` (for recurrence math)
- **Architecture**: Service-Repository (Extension of current Phase I structure)

## Data Model Updates
### Task Model (Pydantic)
- `priority`: `PriorityEnum` (HIGH, MEDIUM, LOW)
- `tags`: `List[str]`
- `due_date`: `Optional[datetime]`
- `recurrence`: `Optional[RecurrenceEnum]` (DAILY, WEEKLY)

## Implementation Logic
1. **Filtering**: The `TaskService` will filter the in-memory list using list comprehensions matching tags and priority enums.
2. **Recurrence Engine**: A "post-completion" hook in the `TaskService`. If a task has `recurrence`, the service calculates the next date and calls `repository.add()` for a new task instance.
3. **UI Highlighting**: The `Rich` table formatter will check `due_date < now` to apply `bold red` styles.

## Constitution Check
- [x] Decoupled Architecture: Repository logic remains isolated.
- [x] Type Safety: Using Enums and Pydantic validators.
- [x] Spec-First: This plan precedes implementation.

## Project Structure
- `src/models.py`: Update with Enums and new fields.
- `src/service.py`: Add `filter_tasks` and `handle_recurrence` logic.
- `src/main.py`: Update CLI commands to accept new flags.

## Response snapshot

I've completed the architectural planning for the "Todo Organization & Intelligence" feature. I performed Phase 0 research (selecting `python-dateutil` for recurrence and `Pydantic` Enums for validation) and Phase 1 design (creating the data model, CLI contracts, and quickstart guide). The implementation plan is now finalized in `specs/003-todo-org-intel/plan.md`.

## Outcome

- ✅ Impact: Provided a detailed technical roadmap for evolving the application's intelligence and organization capabilities.
- 🧪 Tests: No tests run; this was a design phase.
- 📁 Files: Generated `plan.md`, `research.md`, `data-model.md`, `cli.md`, and `quickstart.md`.
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: Building on the existing Phase I structure allowed for a clean extension of the Service-Repository pattern. Decoupling the Intelligence Engine as a service-layer responsibility maintains the purity of the repository.

## Evaluation notes (flywheel)

- Failure modes observed: None during this phase.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
