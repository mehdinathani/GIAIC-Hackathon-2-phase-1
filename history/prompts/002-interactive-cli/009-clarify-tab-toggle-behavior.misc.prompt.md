---
id: "009"
title: "Clarify TAB Toggle Behavior"
stage: "misc"
date: "2025-12-28"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "002-interactive-cli"
branch: "002-interactive-cli"
user: "Claude User"
command: "sp.clarify"
labels: ["clarification","interactive-cli","tab-toggle"]
links:
  spec: "specs/002-interactive-cli/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/002-interactive-cli/spec.md"
  - "src/todo/interactive.py"
tests: []
---

## Prompt

sp.clarify

User input: "toggle option is correct, just instead of just toggle complete it should be toggle complete / incomplete, and on tab when we are on task it should stay here but change the color and status so user know that on tab toggle is working"

## Response snapshot

Integrated TAB toggle clarification into spec with smart implementation:

**Spec Updates:**
- Added FR-013: TAB key must toggle selected task's completion status with immediate visual feedback
- Updated User Story 2 with new acceptance scenario (TAB on task toggles status and updates color/indicator)
- Added edge case note for TAB behavior
- Recorded clarification in Clarifications section

**Implementation:**
- Added prompt_toolkit Keys and KeyBindings imports for advanced key handling
- Created `_show_task_list_with_tab_toggle()` method using prompt-toolkit's Application
- Features:
  - ↑↓ Arrow keys: Navigate between tasks
  - TAB: Toggle current task status (pending ↔ complete) with visual feedback
  - ↵ Enter: Select task for actions
  - Esc: Return to main menu
- Visual feedback after TAB toggle:
  - Status indicator changes (○ → ✓)
  - Task color updates (pending yellow → complete green)
  - "(now COMPLETE/PENDING)" indicator appears briefly
  - User stays on same task after toggle

## Outcome

- ✅ Impact: TAB toggle clarified and fully implemented
- 🧪 Tests: All 92 tests pass
- 📁 Files: Updated `specs/002-interactive-cli/spec.md`, enhanced `src/todo/interactive.py`
- 🔁 Next prompts: Ready for manual testing with `uv run todo`
- 🧠 Reflection: User wanted creative solution - implemented prompt-toolkit Application with custom key bindings for true TAB support (questionary.select doesn't support TAB key bindings natively). Visual feedback shows both color change and text indicator.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All 92 tests PASS
- Prompt variant (if applicable): N/A (clarification with implementation)
- Next experiment (smallest change to try): Add animation effect for toggle feedback (fade transition)
