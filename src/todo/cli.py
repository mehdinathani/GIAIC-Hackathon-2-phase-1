"""CLI layer for Todo Application using Typer and Rich."""

from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from todo.exceptions import TaskNotFoundError
from todo.interactive import InteractiveApp
from todo.models import TaskCreate, TaskUpdate
from todo.repository import InMemoryTaskRepository
from todo.service import TaskService

# Initialize the application components
_repository = InMemoryTaskRepository()
_service = TaskService(repository=_repository)

# Rich console for formatted output
console = Console()

# Typer application
app = typer.Typer(
    name="todo",
    help="A simple in-memory todo list manager.",
    add_completion=False,
    invoke_without_command=True,
)


@app.callback()
def main_callback(ctx: typer.Context) -> None:
    """Callback invoked when no subcommand is provided.

    Launches the interactive menu mode.
    """
    if ctx.invoked_subcommand is None:
        launch_interactive()


def launch_interactive() -> None:
    """Launch the interactive menu mode."""
    interactive_app = InteractiveApp(service=_service)
    interactive_app.run()


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="Title of the task")],
    description: Annotated[
        str | None, typer.Option("--description", "-d", help="Task description")
    ] = None,
) -> None:
    """Create a new task."""
    try:
        data = TaskCreate(title=title, description=description)
        task = _service.create_task(data)

        panel_content = f"[bold]ID:[/bold] {task.id}\n"
        panel_content += f"[bold]Title:[/bold] {task.title}\n"
        if task.description:
            panel_content += f"[bold]Description:[/bold] {task.description}\n"
        panel_content += "[bold]Status:[/bold] [yellow]Pending[/yellow]\n"
        panel_content += (
            f"[bold]Created:[/bold] {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        console.print(
            Panel(
                panel_content, title="[green]Task Created[/green]", border_style="green"
            )
        )
    except ValueError as e:
        console.print(
            Panel(str(e), title="[red]Validation Error[/red]", border_style="red")
        )
        raise typer.Exit(code=1) from None


@app.command("list")
def list_tasks() -> None:
    """Display all tasks in a formatted table."""
    tasks = _service.list_tasks()

    if not tasks:
        console.print(
            Panel(
                "No tasks found. Add one with: [bold]todo add[/bold]",
                title="[blue]Info[/blue]",
                border_style="blue",
            )
        )
        return

    table = Table(title=None)
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Created", style="dim")

    for task in tasks:
        status = (
            "[green]Completed[/green]" if task.completed else "[yellow]Pending[/yellow]"
        )
        table.add_row(
            str(task.id),
            task.title,
            status,
            task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

    console.print(table)


@app.command()
def complete(
    task_id: Annotated[int, typer.Argument(help="ID of the task to complete")],
) -> None:
    """Mark a task as completed."""
    try:
        task = _service.complete_task(task_id)
        console.print(
            Panel(
                f"Task {task.id} marked as completed\n[bold]Title:[/bold] {task.title}",
                title="[green]Task Completed[/green]",
                border_style="green",
            )
        )
    except TaskNotFoundError as e:
        console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
        raise typer.Exit(code=1) from None


@app.command()
def delete(
    task_id: Annotated[int, typer.Argument(help="ID of the task to delete")],
) -> None:
    """Delete a task permanently."""
    try:
        _service.delete_task(task_id)
        console.print(
            Panel(
                f"Task {task_id} has been deleted",
                title="[green]Task Deleted[/green]",
                border_style="green",
            )
        )
    except TaskNotFoundError as e:
        console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
        raise typer.Exit(code=1) from None


@app.command()
def update(
    task_id: Annotated[int, typer.Argument(help="ID of the task to update")],
    title: Annotated[
        str | None, typer.Option("--title", "-t", help="New title")
    ] = None,
    description: Annotated[
        str | None, typer.Option("--description", "-d", help="New description")
    ] = None,
) -> None:
    """Update an existing task's title and/or description."""
    if title is None and description is None:
        console.print(
            Panel(
                "At least one of --title or --description must be provided",
                title="[red]Validation Error[/red]",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    try:
        data = TaskUpdate(title=title, description=description)
        task = _service.update_task(task_id, data)

        panel_content = f"[bold]ID:[/bold] {task.id}\n"
        panel_content += f"[bold]Title:[/bold] {task.title}\n"
        if task.description:
            panel_content += f"[bold]Description:[/bold] {task.description}\n"
        status = "Completed" if task.completed else "Pending"
        panel_content += f"[bold]Status:[/bold] {status}"

        console.print(
            Panel(
                panel_content, title="[green]Task Updated[/green]", border_style="green"
            )
        )
    except TaskNotFoundError as e:
        console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
        raise typer.Exit(code=1) from None
    except ValueError as e:
        console.print(
            Panel(str(e), title="[red]Validation Error[/red]", border_style="red")
        )
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
