"""Integration tests for advanced Todo features (Priority, Tags, Search, Filter, Sort)."""

import pytest
from pathlib import Path
from typer.testing import CliRunner
from datetime import datetime, timedelta

from todo import cli
from todo.models import PriorityEnum


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture(autouse=True)
def reset_app_state(tmp_path: Path) -> None:
    """Reset the application state before each test."""
    test_file = tmp_path / "test_advanced_tasks.json"
    cli._repository = cli.FileTaskRepository(file_path=str(test_file))
    cli._service = cli.TaskService(repository=cli._repository)


class TestTaskOrganization:
    """Tests for US1: Task Organization (Priorities and Tags)."""

    def test_add_task_with_priority_and_tags(self, runner: CliRunner) -> None:
        """Should create a task with priority and tags."""
        result = runner.invoke(
            cli.app, ["add", "Priority Task", "-p", "HIGH", "-t", "#urgent", "-t", "#work"]
        )
        assert result.exit_code == 0
        assert "HIGH" in result.output
        assert "#urgent #work" in result.output

    def test_update_priority_and_tags(self, runner: CliRunner) -> None:
        """Should update task priority and tags."""
        runner.invoke(cli.app, ["add", "Old Task"])
        result = runner.invoke(
            cli.app, ["update", "1", "-p", "MEDIUM", "-T", "#home"]
        )
        assert result.exit_code == 0
        assert "MEDIUM" in result.output
        assert "#home" in result.output


class TestSearchFilterSort:
    """Tests for US2: Search, Filter, and Sort."""

    def test_filter_priority(self, runner: CliRunner) -> None:
        """Should filter tasks by priority."""
        runner.invoke(cli.app, ["add", "High Task", "-p", "HIGH"])
        runner.invoke(cli.app, ["add", "Low Task", "-p", "LOW"])

        result = runner.invoke(cli.app, ["list", "--filter-priority", "HIGH"])
        assert "High Task" in result.output
        assert "Low Task" not in result.output

    def test_filter_tag(self, runner: CliRunner) -> None:
        """Should filter tasks by tag."""
        runner.invoke(cli.app, ["add", "Work Task", "-t", "#work"])
        runner.invoke(cli.app, ["add", "Home Task", "-t", "#home"])

        result = runner.invoke(cli.app, ["list", "--filter-tag", "#work"])
        assert "Work Task" in result.output
        assert "Home Task" not in result.output

    def test_filter_status(self, runner: CliRunner) -> None:
        """Should filter tasks by status."""
        runner.invoke(cli.app, ["add", "Done Task"])
        runner.invoke(cli.app, ["add", "Todo Task"])
        runner.invoke(cli.app, ["complete", "1"])

        # Filter pending (False)
        result = runner.invoke(cli.app, ["list", "--filter-status", "pending"])
        assert "Todo Task" in result.output
        assert "Done Task" not in result.output

        # Filter completed (True)
        result = runner.invoke(cli.app, ["list", "--filter-status", "completed"])
        assert "Done Task" in result.output
        assert "Todo Task" not in result.output

    def test_search(self, runner: CliRunner) -> None:
        """Should search tasks by keyword."""
        runner.invoke(cli.app, ["add", "Buy milk", "-d", "grocery store"])
        runner.invoke(cli.app, ["add", "Call mom"])

        result = runner.invoke(cli.app, ["list", "--search", "milk"])
        assert "Buy milk" in result.output
        assert "Call mom" not in result.output

        result = runner.invoke(cli.app, ["list", "--search", "store"])
        assert "Buy milk" in result.output

    def test_sort_priority(self, runner: CliRunner) -> None:
        """Should sort tasks by priority (HIGH > MEDIUM > LOW)."""
        runner.invoke(cli.app, ["add", "Low", "-p", "LOW"])
        runner.invoke(cli.app, ["add", "High", "-p", "HIGH"])
        runner.invoke(cli.app, ["add", "Medium", "-p", "MEDIUM"])

        result = runner.invoke(cli.app, ["list", "--sort", "priority"])
        # In a table, High should appear before Medium should appear before Low
        output = result.output
        assert output.find("High") < output.find("Medium") < output.find("Low")

    def test_sort_due_date(self, runner: CliRunner) -> None:
        """Should sort tasks by due date."""
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        runner.invoke(cli.app, ["add", "Later", "--due", tomorrow])
        runner.invoke(cli.app, ["add", "Sooner", "--due", today])
        runner.invoke(cli.app, ["add", "No Due"])

        result = runner.invoke(cli.app, ["list", "--sort", "due"])
        output = result.output
        # Correct order: Sooner, Later, No Due
        assert output.find("Sooner") < output.find("Later") < output.find("No Due")

    def test_overdue_highlighting(self, runner: CliRunner) -> None:
        """Should show Overdue status for overdue tasks."""
        past_due = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        runner.invoke(cli.app, ["add", "Overdue Task", "--due", past_due])

        result = runner.invoke(cli.app, ["list"])
        assert "Overdue Task" in result.output
        assert "Overdue" in result.output
