"""Interactive menu-driven interface for the Todo CLI Application.

This module provides an interactive menu system using questionary for prompts
and Rich for formatted output. Users can navigate menus with arrow keys,
select tasks from lists, and perform CRUD operations through a guided interface.

The interactive mode is launched when the CLI is invoked without subcommands,
providing a user-friendly alternative to the command-line arguments.
"""

import os
import sys
from enum import Enum
from typing import TYPE_CHECKING

import questionary
from prompt_toolkit.styles import Style as QuestionaryStyle
from rich.console import Console
from rich.panel import Panel

if TYPE_CHECKING:
    from todo.models import Task
    from todo.service import TaskService


class MenuAction(str, Enum):
    """Menu actions available in the main menu."""

    ADD_TASK = "add_task"
    VIEW_LIST = "view_list"
    TOGGLE_COMPLETE = "toggle_complete"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    EXIT = "exit"


class TaskAction(str, Enum):
    """Actions available in the task context menu."""

    TOGGLE_COMPLETE = "toggle_complete"
    UPDATE = "update"
    DELETE = "delete"
    BACK = "back"


# Custom questionary Style for consistent highlighting with chalk color scheme
QUESTIONARY_STYLE: QuestionaryStyle = QuestionaryStyle(
    [
        ("question", "bold cyan"),
        ("answer", "bold green"),
        ("pointer", "bold cyan"),
        ("highlighted", "bold cyan"),
        ("selected", "fg:#00aaaa bold"),
        ("header", "bold"),
        ("footer", "dim"),
    ]
)


# Color scheme for Rich output (consistent with chalk color palette)
class ColorScheme:
    """Color constants for consistent UI styling per chalk color scheme."""

    HIGHLIGHT = "cyan"
    SUCCESS = "green"  # Complete tasks
    ERROR = "red"  # Incomplete/pending tasks
    INFO = "blue"
    PENDING = "red"  # Incomplete = red
    MUTED = "dim"
    COMPLETE = "green"  # Complete = green


class InteractiveApp:
    """Interactive menu application for the Todo CLI.

    This class provides the main interactive interface, managing menu
    navigation, task selection, and CRUD operations through questionary
    prompts and Rich formatted output.

    Args:
        service: TaskService instance for business logic operations.
    """

    def __init__(self, service: "TaskService") -> None:
        self._service = service
        self._console = Console()

    def _get_menu_choices(self) -> list[dict[str, str]]:
        """Return the list of menu options for the main menu.

        Returns:
            List of dictionaries with 'name' (display) and 'value' (action) keys.
        """
        return [
            {"name": "Add Task", "value": MenuAction.ADD_TASK.value},
            {"name": "View Task List", "value": MenuAction.VIEW_LIST.value},
            {"name": "Toggle Complete", "value": MenuAction.TOGGLE_COMPLETE.value},
            {"name": "Update Task", "value": MenuAction.UPDATE_TASK.value},
            {"name": "Delete Task", "value": MenuAction.DELETE_TASK.value},
            {"name": "Exit", "value": MenuAction.EXIT.value},
        ]

    def _get_task_actions(self) -> list[dict[str, str]]:
        """Return the list of actions for the task context menu.

        Returns:
            List of dictionaries with 'name' (display) and 'value' (action) keys.
        """
        return [
            {"name": "Toggle Complete", "value": TaskAction.TOGGLE_COMPLETE.value},
            {"name": "Update", "value": TaskAction.UPDATE.value},
            {"name": "Delete", "value": TaskAction.DELETE.value},
            {"name": "Back to List", "value": TaskAction.BACK.value},
        ]

    def _format_task_choice(self, task: "Task") -> str:
        """Format a task for display in a selectable list.

        Args:
            task: The task to format.

        Returns:
            Formatted string representation of the task.
        """
        status = (
            "[green]Completed[/green]" if task.completed else "[yellow]Pending[/yellow]"
        )
        date = task.created_at.strftime("%Y-%m-%d")
        return f"[{task.id}] {task.title:<30} {status:<12} {date}"

    def show_main_menu(self) -> str | None:
        """Display the main menu and wait for user selection.

        Returns:
            The selected action value, or None if cancelled.
        """
        choices = self._get_menu_choices()
        names = [c["name"] for c in choices]
        values = [c["value"] for c in choices]

        try:
            selected = questionary.select(
                "What would you like to do?",
                choices=names,
                style=QUESTIONARY_STYLE,
            ).ask()

            if selected is None:
                return None

            index = names.index(selected)
            return values[index]
        except KeyboardInterrupt:
            return None

    def run(self) -> None:
        """Run the main interactive loop."""
        while True:
            try:
                action = self.show_main_menu()

                if action is None or action == MenuAction.EXIT.value:
                    self._handle_exit()
                    break
                elif action == MenuAction.ADD_TASK.value:
                    self.handle_add_task()
                elif action == MenuAction.VIEW_LIST.value:
                    self.handle_view_list()
                elif action == MenuAction.TOGGLE_COMPLETE.value:
                    self.handle_toggle_complete()
                elif action == MenuAction.UPDATE_TASK.value:
                    self.handle_update_task()
                elif action == MenuAction.DELETE_TASK.value:
                    self.handle_delete_task()
            except KeyboardInterrupt:
                self._handle_exit()
                break

    def _handle_exit(self) -> None:
        """Handle application exit with goodbye message."""
        print_success(
            "Thanks for using TODO! Your tasks are waiting for you next time."
        )
        sys.exit(0)

    def show_task_list(self) -> "Task | None":
        """Display the list of tasks for selection with TAB toggle support.

        Returns:
            The selected task, or None if cancelled/empty.
        """
        tasks = self._service.list_tasks()

        if not tasks:
            print_info("No tasks found. Would you like to add one?")
            return None

        return self._show_task_list_with_tab_toggle(tasks)

    def _format_task_for_display(self, task: "Task", selected: bool = False) -> str:
        """Format a task for display with status indicator and color hints.

        Args:
            task: The task to format.
            selected: Whether this task is currently selected.

        Returns:
            Formatted task string with status indicator.
        """
        status = "✓" if task.completed else "○"
        status_color = ColorScheme.SUCCESS if task.completed else ColorScheme.PENDING
        title = task.title[:40] + "..." if len(task.title) > 40 else task.title
        return f"[{status_color}]{status}[/] {title}"

    def _show_task_list_with_tab_toggle(self, tasks: list["Task"]) -> "Task | None":
        """Display task list with TAB key toggle support.

        Uses a simple console-based approach with:
        - Arrow keys (↑↓): Navigate between tasks
        - TAB: Toggle current task's completion status with visual feedback
        - Enter: Select task for actions
        - Escape: Return to main menu

        Args:
            tasks: List of tasks to display.

        Returns:
            The selected task, or None if cancelled.
        """
        import sys

        # Cross-platform key input
        if os.name == "nt":
            # Windows: use msvcrt
            import msvcrt
        else:
            # Unix: use termios/tty
            import termios
            import tty

        current_index = 0
        toggled_index = None  # Track which task was just toggled for feedback

        def get_task_lines() -> list[str]:
            """Generate formatted task lines for display."""
            lines = []
            for i, task in enumerate(tasks):
                if i == current_index:
                    # Selected task - show with highlight color
                    status = "✓" if task.completed else "○"
                    title = (
                        task.title[:38] + "..." if len(task.title) > 38 else task.title
                    )
                    lines.append(
                        f"[{ColorScheme.HIGHLIGHT}]▶ {status} {title}[/] (TAB to toggle)"
                    )
                elif i == toggled_index:
                    # Recently toggled task - flash effect
                    status = "✓" if task.completed else "○"
                    title = (
                        task.title[:38] + "..." if len(task.title) > 38 else task.title
                    )
                    new_status = "COMPLETE" if task.completed else "PENDING"
                    lines.append(
                        f"[{ColorScheme.SUCCESS}]  {status} {title}[/] [{ColorScheme.INFO}](now {new_status})[/]"
                    )
                else:
                    # Regular task
                    status = "✓" if task.completed else "○"
                    title = (
                        task.title[:40] + "..." if len(task.title) > 40 else task.title
                    )
                    lines.append(f"  {status} {title}")
            return lines

        def render_display() -> None:
            """Render the task list display."""
            clear_screen()
            print_header("Select a Task")
            lines = get_task_lines()
            for line in lines:
                print(f"  {line}")
            print()
            print_info("↑↓ Navigate  TAB Toggle  ↵ Select  Esc Back")

        def get_key() -> str:
            """Get a key press and return the key name."""
            if os.name == "nt":
                # Windows implementation
                ch = msvcrt.getch()
                if ch == b"\xe0":  # Arrow key prefix
                    arrow = msvcrt.getch()
                    if arrow == b"H":
                        return "up"
                    elif arrow == b"P":
                        return "down"
                    elif arrow == b"M":
                        return "right"
                    elif arrow == b"K":
                        return "left"
                elif ch == b"\t":
                    return "tab"
                elif ch == b"\r":
                    return "enter"
                elif ch == b"\x1b":
                    return "escape"
                elif ch == b"\x03":
                    raise KeyboardInterrupt
                return ch.decode("utf-8", errors="ignore")
            else:
                # Unix implementation
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    if key == "\x1b":  # Escape sequence
                        extra = sys.stdin.read(2)
                        if extra == "[A":
                            return "up"
                        elif extra == "[B":
                            return "down"
                        elif extra == "[C":
                            return "right"
                        elif extra == "[D":
                            return "left"
                        return "escape"
                    elif key == "\t":
                        return "tab"
                    elif key == "\r":
                        return "enter"
                    elif key == "\x03":
                        raise KeyboardInterrupt
                    return key
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        while True:
            render_display()

            try:
                key = get_key()
            except KeyboardInterrupt:
                return None

            if key == "down":
                if current_index < len(tasks) - 1:
                    current_index += 1
                    toggled_index = None
            elif key == "up":
                if current_index > 0:
                    current_index -= 1
                    toggled_index = None
            elif key == "tab":
                task = tasks[current_index]
                self._service.toggle_complete_task(task.id)
                # Reload tasks to get updated state
                tasks[current_index] = self._service.get_task(task.id)
                toggled_index = current_index
            elif key == "enter":
                return tasks[current_index]
            elif key == "escape":
                return None
            # Other keys ignored

    def show_task_actions(self, task: "Task") -> str | None:
        """Display the context menu for a task.

        Args:
            task: The task to show actions for.

        Returns:
            The selected action, or None if cancelled.
        """
        choices = self._get_task_actions()
        names = [c["name"] for c in choices]
        values = [c["value"] for c in choices]

        try:
            selected = questionary.select(
                "What would you like to do with this task?",
                choices=names,
                style=QUESTIONARY_STYLE,
            ).ask()

            if selected is None:
                return None

            index = names.index(selected)
            return values[index]
        except KeyboardInterrupt:
            return None

    def prompt_task_title(self) -> str | None:
        """Prompt for a new task title.

        Returns:
            The entered title, or None if cancelled.
        """
        try:
            title = questionary.text(
                "Enter task title:",
                style=QUESTIONARY_STYLE,
            ).ask()
            return title if title else None
        except KeyboardInterrupt:
            return None

    def prompt_task_description(self) -> str | None:
        """Prompt for an optional task description.

        Returns:
            The entered description, or empty string if skipped/cancelled.
        """
        try:
            description = questionary.text(
                "Enter description (optional):",
                style=QUESTIONARY_STYLE,
            ).ask()
            return description if description else ""
        except KeyboardInterrupt:
            return ""

    def handle_add_task(self) -> None:
        """Handle the add task workflow."""
        title = self.prompt_task_title()
        if title is None:
            print_info("Task creation cancelled.")
            return

        description = self.prompt_task_description()

        from todo.models import TaskCreate

        data = TaskCreate(title=title, description=description if description else None)
        task = self._service.create_task(data)

        content = f"[bold]ID:[/bold] {task.id}\n"
        content += f"[bold]Title:[/bold] {task.title}\n"
        if task.description:
            content += f"[bold]Description:[/bold] {task.description}\n"
        content += "[bold]Status:[/bold] [yellow]Pending[/yellow]\n"
        content += (
            f"[bold]Created:[/bold] {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        print_success(content)

    def handle_view_list(self) -> None:
        """Handle viewing the task list and selecting a task."""
        task = self.show_task_list()
        if task is None:
            return

        while True:
            action = self.show_task_actions(task)
            if action is None or action == TaskAction.BACK.value:
                break

            if action == TaskAction.TOGGLE_COMPLETE.value:
                self.handle_toggle_complete(task)
            elif action == TaskAction.UPDATE.value:
                self.handle_update_task(task)
            elif action == TaskAction.DELETE.value:
                self.handle_delete_task(task)

            task = self._service.get_task(task.id)

    def handle_toggle_complete(self, task: "Task | None" = None) -> None:
        """Handle toggling task completion status bidirectionally.

        Toggles between complete (green) and incomplete (red).
        If task is pending, mark as complete. If task is complete, mark as pending.

        Args:
            task: Optional pre-selected task. If None, prompts for selection.
        """
        if task is None:
            task = self.show_task_list()
            if task is None:
                return

        toggled_task = self._service.toggle_complete_task(task.id)
        if toggled_task.completed:
            print_success(
                f"Task {toggled_task.id} marked as complete\n[bold]Title:[/bold] {toggled_task.title}"
            )
        else:
            print_info(
                f"Task {toggled_task.id} marked as incomplete\n[bold]Title:[/bold] {toggled_task.title}"
            )

    def handle_update_task(self, task: "Task | None" = None) -> None:
        """Handle updating a task.

        Args:
            task: Optional pre-selected task. If None, prompts for selection.
        """
        if task is None:
            task = self.show_task_list()
            if task is None:
                return

        new_title = questionary.text(
            "Enter new title (or press Enter to keep current):",
            default=task.title,
            style=QUESTIONARY_STYLE,
        ).ask()

        if new_title is None:
            new_title = task.title

        new_description = questionary.text(
            "Enter new description (or press Enter to keep current):",
            default=task.description or "",
            style=QUESTIONARY_STYLE,
        ).ask()

        if new_description is None:
            new_description = task.description

        from todo.models import TaskUpdate

        data = TaskUpdate(
            title=new_title if new_title != task.title else None,
            description=new_description
            if new_description != task.description
            else None,
        )

        updated_task = self._service.update_task(task.id, data)

        content = f"[bold]ID:[/bold] {updated_task.id}\n"
        content += f"[bold]Title:[/bold] {updated_task.title}\n"
        if updated_task.description:
            content += f"[bold]Description:[/bold] {updated_task.description}\n"
        status = "Completed" if updated_task.completed else "Pending"
        content += f"[bold]Status:[/bold] {status}"

        print_success(content)

    def handle_delete_task(self, task: "Task | None" = None) -> None:
        """Handle deleting a task with confirmation.

        Args:
            task: Optional pre-selected task. If None, prompts for selection.
        """
        if task is None:
            task = self.show_task_list()
            if task is None:
                return

        content = f"[bold]Title:[/bold] {task.title}\n"
        if task.description:
            content += f"[bold]Description:[/bold] {task.description}\n"
        content += "\n[red]This action cannot be undone![/red]"

        print_error(content)

        try:
            confirm = questionary.confirm(
                "Are you sure you want to delete this task?",
                default=False,
                style=QUESTIONARY_STYLE,
            ).ask()

            if confirm:
                self._service.delete_task(task.id)
                print_success(f"Task {task.id} has been deleted")
            else:
                print_info("Delete cancelled.")
        except KeyboardInterrupt:
            print_info("Delete cancelled.")


# =============================================================================
# Utility Functions
# =============================================================================


def clear_screen() -> None:
    """Clear the terminal screen for a fresh display."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str) -> None:
    """Print a centered header with decorative borders.

    Args:
        title: The header text to display.
    """
    console = Console()
    border = "=" * (len(title) + 4)
    content = f"\n{title.center(len(title) + 2)}\n"
    panel = Panel(
        content,
        title=f"[bold]{title}[/bold]",
        subtitle=border,
        border_style=ColorScheme.HIGHLIGHT,
    )
    console.print(panel)


def print_success(message: str) -> None:
    """Print a success message in a green panel.

    Args:
        message: The success message to display.
    """
    console = Console()
    console.print(
        Panel(message, title="[green]Success[/green]", border_style=ColorScheme.SUCCESS)
    )


def print_error(message: str) -> None:
    """Print an error message in a red panel.

    Args:
        message: The error message to display.
    """
    console = Console()
    console.print(
        Panel(message, title="[red]Error[/red]", border_style=ColorScheme.ERROR)
    )


def print_info(message: str) -> None:
    """Print an info message in a blue panel.

    Args:
        message: The info message to display.
    """
    console = Console()
    console.print(
        Panel(message, title="[blue]Info[/blue]", border_style=ColorScheme.INFO)
    )


def wait_for_enter() -> None:
    """Wait for the user to press Enter before continuing."""
    input("\nPress Enter to continue...")
