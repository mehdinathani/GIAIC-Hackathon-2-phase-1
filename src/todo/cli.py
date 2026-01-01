"""CLI layer for Todo Application using Typer and Rich."""

from datetime import datetime
from typing import Annotated

import typer
from rich.panel import Panel

from todo import ui
from todo.exceptions import TaskNotFoundError
from todo.interactive import InteractiveApp
from todo.models import PriorityEnum, RecurrenceEnum, TaskCreate, TaskUpdate
from todo.repository import InMemoryTaskRepository
from todo.service import TaskService

# Initialize the application components
_repository = InMemoryTaskRepository()
_service = TaskService(repository=_repository)

# Typer application
app = typer.Typer(
    name="todo",
    help="A simple in-memory todo list manager with organization and intelligence.",
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
    priority: Annotated[
        PriorityEnum, typer.Option("--priority", "-p", help="Task priority")
    ] = PriorityEnum.LOW,
    tags: Annotated[
        list[str] | None, typer.Option("--tag", "-t", help="Task tags (can be repeated)")
    ] = None,
    due: Annotated[
        datetime | None, typer.Option("--due", help="Due date (YYYY-MM-DD [HH:MM:SS])")
    ] = None,
    recur: Annotated[
        RecurrenceEnum, typer.Option("--recur", help="Recurrence rule")
    ] = RecurrenceEnum.NONE,
) -> None:
    """Create a new task."""
    try:
        data = TaskCreate(
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due,
            recurrence=recur,
        )
        task = _service.create_task(data)
        ui.render_task_detail(task, title="Task Created", border_style="green")
    except ValueError as e:
        ui.console.print(
            Panel(str(e), title="[red]Validation Error[/red]", border_style="red")
        )
        raise typer.Exit(code=1) from None


@app.command("list")
def list_tasks(
    filter_priority: Annotated[
        PriorityEnum | None,
        typer.Option("--filter-priority", "-p", help="Filter by priority"),
    ] = None,
    filter_tag: Annotated[
        str | None, typer.Option("--filter-tag", "-t", help="Filter by tag")
    ] = None,
    search: Annotated[
        str | None, typer.Option("--search", "-s", help="Search in title/description")
    ] = None,
    sort_by: Annotated[
        str | None, typer.Option("--sort", help="Sort by: priority, due, title")
    ] = None,
) -> None:
    """Display tasks with optional filtering and sorting."""
    tasks = _service.list_tasks(
        filter_priority=filter_priority,
        filter_tag=filter_tag,
        search_query=search,
        sort_by=sort_by,
    )
    ui.render_task_list(tasks)


@app.command()
def complete(
    task_id: Annotated[int, typer.Argument(help="ID of the task to complete")],
) -> None:
    """Mark a task as completed."""
    try:
        task = _service.complete_task(task_id)
        ui.render_task_detail(task, title="Task Completed", border_style="green")
    except TaskNotFoundError as e:
        ui.console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
        raise typer.Exit(code=1) from None


@app.command()
def delete(
    task_id: Annotated[int, typer.Argument(help="ID of the task to delete")],
) -> None:
    """Delete a task permanently."""
    try:
        _service.delete_task(task_id)
        ui.console.print(
            Panel(
                f"Task {task_id} has been deleted",
                title="[green]Task Deleted[/green]",
                border_style="green",
            )
        )
    except TaskNotFoundError as e:
        ui.console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
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
    priority: Annotated[
        PriorityEnum | None, typer.Option("--priority", "-p", help="New priority")
    ] = None,
    tags: Annotated[
        list[str] | None, typer.Option("--tag", "-T", help="New tags (replaces existing)")
    ] = None,
    due: Annotated[
        datetime | None, typer.Option("--due", help="New due date")
    ] = None,
    recur: Annotated[
        RecurrenceEnum | None, typer.Option("--recur", help="New recurrence rule")
    ] = None,
) -> None:
    """Update an existing task."""
    if all(v is None for v in [title, description, priority, tags, due, recur]):
        ui.console.print(
            Panel(
                "At least one option (--title, --description, --priority, --tag, --due, or --recur) must be provided.",
                title="[red]Validation Error[/red]",
                border_style="red",
            )
        )
        raise typer.Exit(code=1)

    try:
        data = TaskUpdate(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due,
            recurrence=recur,
        )
        task = _service.update_task(task_id, data)
        ui.render_task_detail(task, title="Task Updated", border_style="green")
    except TaskNotFoundError as e:
        ui.console.print(Panel(str(e), title="[red]Error[/red]", border_style="red"))
        raise typer.Exit(code=1) from None
    except ValueError as e:
        ui.console.print(
            Panel(str(e), title="[red]Validation Error[/red]", border_style="red")
        )
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
