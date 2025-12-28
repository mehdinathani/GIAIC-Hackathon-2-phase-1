"""Integration tests for CLI commands using Typer testing utilities."""

import pytest
from typer.testing import CliRunner

from todo import cli


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture(autouse=True)
def reset_app_state() -> None:
    """Reset the application state before each test.

    This is necessary because the CLI module uses module-level state.
    """
    cli._repository._tasks.clear()
    cli._repository._next_id = 1


class TestAddCommand:
    """Tests for the 'add' command."""

    def test_add_simple_task(self, runner: CliRunner) -> None:
        """Add command should create a task with just a title."""
        result = runner.invoke(cli.app, ["add", "Buy milk"])
        assert result.exit_code == 0
        assert "Task Created" in result.output
        assert "Buy milk" in result.output
        assert "ID" in result.output

    def test_add_task_with_description(self, runner: CliRunner) -> None:
        """Add command should accept --description option."""
        result = runner.invoke(
            cli.app, ["add", "Buy milk", "-d", "2% from grocery store"]
        )
        assert result.exit_code == 0
        assert "Buy milk" in result.output
        assert "2% from grocery store" in result.output

    def test_add_empty_title_fails(self, runner: CliRunner) -> None:
        """Add command should fail with empty title."""
        result = runner.invoke(cli.app, ["add", "   "])
        assert result.exit_code == 1
        assert "Validation Error" in result.output

    def test_add_shows_pending_status(self, runner: CliRunner) -> None:
        """Add command should show Pending status."""
        result = runner.invoke(cli.app, ["add", "New task"])
        assert result.exit_code == 0
        assert "Pending" in result.output


class TestListCommand:
    """Tests for the 'list' command."""

    def test_list_empty(self, runner: CliRunner) -> None:
        """List command should show info message when no tasks."""
        result = runner.invoke(cli.app, ["list"])
        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_list_with_tasks(self, runner: CliRunner) -> None:
        """List command should display all tasks in a table."""
        runner.invoke(cli.app, ["add", "Task 1"])
        runner.invoke(cli.app, ["add", "Task 2"])

        result = runner.invoke(cli.app, ["list"])
        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" in result.output
        assert "ID" in result.output

    def test_list_shows_status(self, runner: CliRunner) -> None:
        """List command should show task status."""
        runner.invoke(cli.app, ["add", "Task 1"])
        result = runner.invoke(cli.app, ["list"])
        assert result.exit_code == 0
        assert "Pending" in result.output

    def test_list_shows_completed_status(self, runner: CliRunner) -> None:
        """List command should show Completed status for completed tasks."""
        runner.invoke(cli.app, ["add", "Task 1"])
        runner.invoke(cli.app, ["complete", "1"])

        result = runner.invoke(cli.app, ["list"])
        assert result.exit_code == 0
        assert "Completed" in result.output


class TestCompleteCommand:
    """Tests for the 'complete' command (mark as complete)."""

    def test_complete_existing_task(self, runner: CliRunner) -> None:
        """Complete command should mark task as completed."""
        runner.invoke(cli.app, ["add", "Task to complete"])
        result = runner.invoke(cli.app, ["complete", "1"])
        assert result.exit_code == 0
        assert "Task Completed" in result.output
        assert "Task to complete" in result.output

    def test_complete_nonexistent_task(self, runner: CliRunner) -> None:
        """Complete command should fail for non-existent task."""
        result = runner.invoke(cli.app, ["complete", "999"])
        assert result.exit_code == 1
        assert "Error" in result.output
        assert "999" in result.output

    def test_complete_shows_in_list(self, runner: CliRunner) -> None:
        """Completed task should show as completed in list."""
        runner.invoke(cli.app, ["add", "Task"])
        runner.invoke(cli.app, ["complete", "1"])

        result = runner.invoke(cli.app, ["list"])
        assert "Completed" in result.output


class TestDeleteCommand:
    """Tests for the 'delete' command."""

    def test_delete_existing_task(self, runner: CliRunner) -> None:
        """Delete command should remove existing task."""
        runner.invoke(cli.app, ["add", "Task to delete"])
        result = runner.invoke(cli.app, ["delete", "1"])
        assert result.exit_code == 0
        assert "Task Deleted" in result.output

    def test_delete_nonexistent_task(self, runner: CliRunner) -> None:
        """Delete command should fail for non-existent task."""
        result = runner.invoke(cli.app, ["delete", "999"])
        assert result.exit_code == 1
        assert "Error" in result.output
        assert "999" in result.output

    def test_delete_removes_from_list(self, runner: CliRunner) -> None:
        """Deleted task should not appear in list."""
        runner.invoke(cli.app, ["add", "Task 1"])
        runner.invoke(cli.app, ["add", "Task 2"])
        runner.invoke(cli.app, ["delete", "1"])

        result = runner.invoke(cli.app, ["list"])
        assert "Task 1" not in result.output
        assert "Task 2" in result.output

    def test_delete_twice_fails(self, runner: CliRunner) -> None:
        """Deleting same task twice should fail."""
        runner.invoke(cli.app, ["add", "Task"])
        runner.invoke(cli.app, ["delete", "1"])

        result = runner.invoke(cli.app, ["delete", "1"])
        assert result.exit_code == 1
        assert "Error" in result.output


class TestUpdateCommand:
    """Tests for the 'update' command."""

    def test_update_title(self, runner: CliRunner) -> None:
        """Update command should change task title."""
        runner.invoke(cli.app, ["add", "Original title"])
        result = runner.invoke(cli.app, ["update", "1", "-t", "New title"])
        assert result.exit_code == 0
        assert "Task Updated" in result.output
        assert "New title" in result.output

    def test_update_description(self, runner: CliRunner) -> None:
        """Update command should change task description."""
        runner.invoke(cli.app, ["add", "Task"])
        result = runner.invoke(cli.app, ["update", "1", "-d", "New description"])
        assert result.exit_code == 0
        assert "Task Updated" in result.output
        assert "New description" in result.output

    def test_update_both(self, runner: CliRunner) -> None:
        """Update command should change both title and description."""
        runner.invoke(cli.app, ["add", "Task"])
        result = runner.invoke(
            cli.app, ["update", "1", "-t", "New title", "-d", "New desc"]
        )
        assert result.exit_code == 0
        assert "New title" in result.output
        assert "New desc" in result.output

    def test_update_requires_at_least_one_option(self, runner: CliRunner) -> None:
        """Update command should fail without any options."""
        runner.invoke(cli.app, ["add", "Task"])
        result = runner.invoke(cli.app, ["update", "1"])
        assert result.exit_code == 1
        assert "Validation Error" in result.output
        assert "at least one" in result.output.lower()

    def test_update_nonexistent_task(self, runner: CliRunner) -> None:
        """Update command should fail for non-existent task."""
        result = runner.invoke(cli.app, ["update", "999", "-t", "New title"])
        assert result.exit_code == 1
        assert "Error" in result.output
        assert "999" in result.output

    def test_update_persists_in_list(self, runner: CliRunner) -> None:
        """Updated task should show new values in list."""
        runner.invoke(cli.app, ["add", "Original"])
        runner.invoke(cli.app, ["update", "1", "-t", "Updated"])

        result = runner.invoke(cli.app, ["list"])
        assert "Updated" in result.output
        assert "Original" not in result.output


class TestHelpCommand:
    """Tests for help output."""

    def test_main_help(self, runner: CliRunner) -> None:
        """Main help should show all commands."""
        result = runner.invoke(cli.app, ["--help"])
        assert result.exit_code == 0
        assert "add" in result.output
        assert "list" in result.output
        assert "complete" in result.output
        assert "update" in result.output
        assert "delete" in result.output

    def test_add_help(self, runner: CliRunner) -> None:
        """Add command help should show options."""
        result = runner.invoke(cli.app, ["add", "--help"])
        assert result.exit_code == 0
        assert "title" in result.output.lower()
        assert "--description" in result.output

    def test_update_help(self, runner: CliRunner) -> None:
        """Update command help should show options."""
        result = runner.invoke(cli.app, ["update", "--help"])
        assert result.exit_code == 0
        assert "--title" in result.output
        assert "--description" in result.output


class TestFullWorkflow:
    """End-to-end workflow tests."""

    def test_complete_task_lifecycle(self, runner: CliRunner) -> None:
        """Test complete CRUD lifecycle."""
        # Create
        result = runner.invoke(cli.app, ["add", "My task", "-d", "Description"])
        assert result.exit_code == 0
        assert "Task Created" in result.output

        # Read
        result = runner.invoke(cli.app, ["list"])
        assert "My task" in result.output
        assert "Pending" in result.output

        # Update
        result = runner.invoke(cli.app, ["update", "1", "-t", "Updated task"])
        assert result.exit_code == 0
        assert "Updated task" in result.output

        # Mark Complete
        result = runner.invoke(cli.app, ["complete", "1"])
        assert result.exit_code == 0
        assert "Task Completed" in result.output

        # Verify completed in list
        result = runner.invoke(cli.app, ["list"])
        assert "Completed" in result.output

        # Delete
        result = runner.invoke(cli.app, ["delete", "1"])
        assert result.exit_code == 0
        assert "Task Deleted" in result.output

        # Verify deleted
        result = runner.invoke(cli.app, ["list"])
        assert "No tasks found" in result.output

    def test_multiple_tasks_workflow(self, runner: CliRunner) -> None:
        """Test managing multiple tasks."""
        # Add three tasks
        runner.invoke(cli.app, ["add", "Task 1"])
        runner.invoke(cli.app, ["add", "Task 2"])
        runner.invoke(cli.app, ["add", "Task 3"])

        # Complete the second task
        runner.invoke(cli.app, ["complete", "2"])

        # Delete the first task
        runner.invoke(cli.app, ["delete", "1"])

        # List should show 2 tasks
        result = runner.invoke(cli.app, ["list"])
        assert "Task 2" in result.output
        assert "Task 3" in result.output
        assert "Task 1" not in result.output
        assert "Completed" in result.output
        assert "Pending" in result.output
