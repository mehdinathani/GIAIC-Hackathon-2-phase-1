# Feature Specification: Interactive CLI Todo App

**Feature Branch**: `002-interactive-cli`
**Created**: 2025-12-28
**Status**: Draft

## Overview

This feature enhances the Phase I CLI Todo application by adding an interactive menu-driven interface. Instead of typing individual commands, users navigate through menus using arrow keys, select tasks from lists, and receive visual feedback - similar to popular npx-based CLI tools.

## User Scenarios & Testing

### User Story 1 - Interactive Main Menu Navigation (Priority: P1)

As a user, I want to see a visually appealing main menu when I launch the app so that I can easily choose what action to perform without memorizing commands.

**Why this priority**: The main menu is the entry point for all interactions.

**Independent Test**: Can be fully tested by launching the app and verifying the menu appears with 5 selectable options.

**Acceptance Scenarios**:

1. **Given** the app is launched, **When** the startup completes, **Then** a main menu displays with 5 options: Add Task, View List, Toggle Complete, Update Task, Delete Task
2. **Given** the main menu is displayed, **When** the user presses arrow keys (Up/Down), **Then** the highlighted option changes accordingly with visual feedback
3. **Given** an option is highlighted, **When** the user presses Enter, **Then** the corresponding action screen is displayed
4. **Given** the main menu is displayed, **When** the user presses q or Escape, **Then** the application exits gracefully

---

### User Story 2 - Interactive Task List Selection (Priority: P2)

As a user, I want to see my tasks in a selectable list so that I can quickly choose a task to complete, update, or delete using arrow keys.

**Why this priority**: Task selection is required for Complete, Update, and Delete operations.

**Independent Test**: Can be fully tested by adding tasks via the menu, then navigating to View List.

**Acceptance Scenarios**:

1. **Given** the user selects View List from main menu, **When** tasks exist, **Then** tasks are displayed in a numbered list with arrow-key selection enabled
2. **Given** the task list is displayed, **When** the user navigates with arrow keys, **Then** the currently selected task is visually highlighted
3. **Given** a task is selected in the list, **When** the user presses Enter, **Then** a context menu appears with options: Toggle Complete, Update, Delete, Back
4. **Given** no tasks exist, **When** the user selects View List, **Then** an informative message is shown with option to add a task
5. **Given** the task list is displayed, **When** the user presses TAB while on a task, **Then** the task's completion status toggles and the task's color/indicator updates immediately to show the new status (user stays on the same task)

---

### User Story 3 - Inline Task Creation with Prompts (Priority: P3)

As a user, I want to add tasks through guided prompts so that I do not need to remember command syntax.

**Why this priority**: Adding tasks is a core function.

**Independent Test**: Can be fully tested by selecting Add Task from menu and following the prompts.

**Acceptance Scenarios**:

1. **Given** the user selects Add Task from main menu, **When** the screen loads, **Then** a prompt appears asking for the task title
2. **Given** the title prompt is displayed, **When** the user enters text and presses Enter, **Then** a second prompt asks for optional description
3. **Given** both prompts are answered, **When** the user confirms, **Then** the task is created and a success message is displayed
4. **Given** any prompt is displayed, **When** the user presses Escape, **Then** the operation is cancelled

---

### User Story 4 - Quick Actions from Task List (Priority: P4)

As a user, I want to perform actions directly from the task list view.

**Why this priority**: Enhances workflow efficiency but requires User Stories 1-2 to be complete first.

**Independent Test**: Can be fully tested by viewing the task list, selecting a task, and performing any action.

**Acceptance Scenarios**:

1. **Given** a task is selected in the list, **When** the user chooses Toggle Complete, **Then** the task status toggles (completed → pending, pending → completed) and updates immediately
2. **Given** a task is selected, **When** the user chooses Update, **Then** inline prompts appear to edit title/description
3. **Given** a task is selected, **When** the user chooses Delete, **Then** a confirmation prompt appears before deletion
4. **Given** an action is completed, **When** the confirmation is dismissed, **Then** the user returns to the updated task list

---

### Edge Cases

- Terminal too small: Display warning message with minimum size requirements
- Keyboard interrupt (Ctrl+C): Exit gracefully with goodbye message
- Unrecognized key: Ignore silently, keep current state
- Navigation at boundaries: Wrap around (Up on first goes to last, Down on last goes to first)
- TAB on last task: Toggle works normally, no navigation change

## Requirements

### Functional Requirements

- **FR-001**: System MUST display an interactive main menu on startup with 5 options
- **FR-002**: System MUST support arrow key navigation (Up/Down) for menu and list selection
- **FR-003**: System MUST highlight the currently selected item with distinct visual styling
- **FR-004**: System MUST allow Enter key to confirm/select the highlighted option
- **FR-005**: System MUST allow Escape key or q to go back/exit from any screen
- **FR-006**: System MUST display tasks in a selectable list format when viewing tasks
- **FR-007**: System MUST provide inline prompts for task creation (title required, description optional)
- **FR-008**: System MUST show a context menu when a task is selected (Toggle Complete, Update, Delete, Back)
- **FR-009**: System MUST display confirmation prompts before destructive actions (delete)
- **FR-010**: System MUST show colored visual feedback using chalk color scheme for success (green), error (red), info (blue), and all UI elements including menus, lists, and prompts
- **FR-011**: System MUST maintain the existing in-memory task storage from Phase I
- **FR-012**: System MUST support wrap-around navigation (first to last, last to first)
- **FR-013**: System MUST support TAB key in task list to toggle the selected task's completion status with immediate visual feedback (color change and status indicator update) while keeping the cursor on the same task

### Key Entities

- **Menu Item**: A selectable option in the main menu (label, action reference)
- **Task List View**: A scrollable, selectable list of Task entities with visual highlight
- **Prompt**: An input field for collecting user text (title, description)
- **Confirmation Dialog**: A yes/no selection prompt before destructive actions

### Assumptions

- Terminal supports ANSI color codes
- Keyboard input can be captured in raw mode for arrow key detection
- Screen can be cleared and redrawn for menu transitions
- Minimum terminal size of 80x24 characters
- Single-user, single-session usage (consistent with Phase I)
- Chalk library available for Python terminal styling (pip install chalk)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can navigate through the main menu and perform any task operation without typing command names
- **SC-002**: Users can complete a full task lifecycle (add, view, complete, delete) in under 60 seconds using only arrow keys and Enter
- **SC-003**: 100 percent of menu options are reachable via keyboard navigation alone
- **SC-004**: Visual feedback (highlighting, colors) is visible on all menu transitions
- **SC-005**: Application responds to key presses within 100ms (perceived as instant)
- **SC-006**: Users can exit from any screen using Escape key within 2 key presses maximum

## Out of Scope

- Mouse/click support (keyboard-only navigation)
- Persistent storage (remains in-memory per Phase I)
- Multi-user or concurrent access
- Configuration file for customizing colors/keybindings
- Task filtering or search functionality
- Undo/redo functionality

## Clarifications

### Session 2025-12-28

- Q: Should "Mark Complete" be a toggle (mark and unmark)? → A: Yes, "Toggle Complete" option should allow both marking and unmarking tasks
- Q: What color library should be used for styling? → A: Use chalk color scheme extensively for all terminal styling
- Q: How should TAB key work for toggle in task list? → A: TAB key toggles task status while staying on the same task; visual feedback (color change + status indicator) confirms the toggle worked
- Q: Toggle Complete should be one button or two (complete/incomplete)? → A: Single "Toggle Complete" button works bidirectionally: pending → complete, complete → pending. No separate "Mark Incomplete" button needed.
- Q: What colors should complete/incomplete tasks display? → A: Complete tasks = green, Incomplete tasks = red. Color applies to status indicator in task list and toggle feedback.
