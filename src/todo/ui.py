"""UI helpers for Todo CLI application."""

from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from todo.models import Task, PriorityEnum

console = Console()

PRIORITY_COLORS = {
    PriorityEnum.HIGH: "bold red",
    PriorityEnum.MEDIUM: "bold yellow",
    PriorityEnum.LOW: "green",
}

def is_overdue(task: Task) -> bool:
    """Check if a task is overdue (not completed and past due date)."""
    if task.completed or task.due_date is None:
        return False
    return task.due_date < datetime.now()

def format_task_status(task: Task) -> str:
    """Format task status with colors."""
    if task.completed:
        return "[green]Completed[/green]"
    if is_overdue(task):
        return "[bold red]Overdue[/bold red]"
    return "[yellow]Pending[/yellow]"

def format_priority(priority: PriorityEnum) -> str:
    """Format priority with colors."""
    color = PRIORITY_COLORS.get(priority, "white")
    return f"[{color}]{priority.value}[/{color}]"

def format_tags(tags: list[str]) -> str:
    """Format tags as a space-separated string."""
    if not tags:
        return ""
    return "[cyan]" + " ".join(tags) + "[/cyan]"

def render_task_list(tasks: list[Task]) -> None:
    """Render a table of tasks."""
    if not tasks:
        console.print(
            Panel(
                "No tasks found.",
                title="[blue]Info[/blue]",
                border_style="blue",
            )
        )
        return

    table = Table(title=None)
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Priority", justify="center")
    table.add_column("Title", style="white")
    table.add_column("Due Date", justify="center")
    table.add_column("Tags", style="cyan")
    table.add_column("Status", justify="center")

    for task in tasks:
        title_style = "bold red" if is_overdue(task) else "white"
        due_date_str = task.due_date.strftime("%Y-%m-%d %H:%M:%S") if task.due_date else "-"

        table.add_row(
            str(task.id),
            format_priority(task.priority),
            f"[{title_style}]{task.title}[/{title_style}]",
            due_date_str,
            format_tags(task.tags),
            format_task_status(task),
        )

    console.print(table)

def render_task_detail(task: Task, title: str = "Task Detail", border_style: str = "green") -> None:
    """Render detailed view of a single task in a panel."""
    content = f"[bold]ID:[/bold] {task.id}\n"
    title_style = "bold red" if is_overdue(task) else "none"
    content += f"[bold]Title:[/bold] [{title_style}]{task.title}[/{title_style}]\n"
    if task.description:
        content += f"[bold]Description:[/bold] {task.description}\n"
    content += f"[bold]Priority:[/bold] {format_priority(task.priority)}\n"
    if task.due_date:
        content += f"[bold]Due Date:[/bold] {task.due_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
    if task.tags:
        content += f"[bold]Tags:[/bold] {format_tags(task.tags)}\n"
    content += f"[bold]Status:[/bold] {format_task_status(task)}\n"
    content += f"[bold]Created:[/bold] {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    console.print(Panel(content, title=f"[{border_style}]{title}[/{border_style}]", border_style=border_style))
