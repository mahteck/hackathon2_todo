"""
CLI display formatting utilities.

Functions for formatting task lists, details, messages, and help text.
"""
from src.models import Task
from datetime import datetime


def format_welcome() -> str:
    """Return welcome banner for application startup."""
    return """
╔════════════════════════════════════════════════╗
║      Todo App - Phase I (Console)             ║
║      Evolution of Todo Project                ║
╚════════════════════════════════════════════════╝

Type 'help' for available commands.
"""


def format_goodbye() -> str:
    """Return goodbye message for application exit."""
    return "Goodbye! Your tasks are not saved (in-memory only)."


def format_success(message: str) -> str:
    """
    Format success message with checkmark.

    Args:
        message: Success message text

    Returns:
        Formatted success message
    """
    return f"✓ {message}"


def format_error(message: str) -> str:
    """
    Format error message with X mark.

    Args:
        message: Error message text

    Returns:
        Formatted error message
    """
    return f"✗ Error: {message}"


def _format_timestamp(iso_timestamp: str) -> str:
    """
    Convert ISO 8601 timestamp to readable format.

    Args:
        iso_timestamp: ISO 8601 timestamp string

    Returns:
        Formatted timestamp (YYYY-MM-DD HH:MM)
    """
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return iso_timestamp  # Return as-is if parsing fails


def _truncate_title(title: str, max_length: int = 50) -> str:
    """
    Truncate title to max length with ellipsis.

    Args:
        title: Task title
        max_length: Maximum length (default 50)

    Returns:
        Truncated title with "..." if exceeded
    """
    if len(title) <= max_length:
        return title
    return title[:max_length - 3] + "..."


def format_task_list(tasks: list[Task]) -> str:
    """
    Format list of tasks as a table.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted table string with headers and summary
    """
    if not tasks:
        return "No tasks found. Use 'add' to create your first task."

    # Table header
    lines = [
        "ID | Status | Title                                      | Created",
        "---+--------+--------------------------------------------+-------------------"
    ]

    # Task rows
    for task in tasks:
        task_id = str(task["id"])
        status = "[✓]" if task["completed"] else "[ ]"
        title = _truncate_title(task["title"], 42)
        created = _format_timestamp(task["created_at"])

        # Format row with proper spacing
        row = f"{task_id:2s} | {status:6s} | {title:42s} | {created}"
        lines.append(row)

    # Summary
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    incomplete = total - completed

    lines.append("")
    lines.append(f"Total: {total} task{'s' if total != 1 else ''} ({completed} completed, {incomplete} incomplete)")

    return "\n".join(lines)


def format_task_detail(task: Task) -> str:
    """
    Format detailed view of a single task.

    Args:
        task: Task object

    Returns:
        Formatted detail string
    """
    status = "Completed" if task["completed"] else "Incomplete"
    description = task["description"] if task["description"] else "None"
    created = _format_timestamp(task["created_at"])
    updated = _format_timestamp(task["updated_at"])

    return f"""Task Details
────────────────────────────────────────
ID:          {task["id"]}
Title:       {task["title"]}
Description: {description}
Status:      {status}
Created:     {created}
Updated:     {updated}"""


def format_help() -> str:
    """Return comprehensive help text with all commands."""
    return """
Todo App - Available Commands
═══════════════════════════════════════════════════════════════

Task Management:
  add <title> [description]
      Create a new task with optional description
      Example: add "Buy groceries" "Milk, eggs, bread"

  list
      Display all tasks in a formatted table
      Example: list

  view <id>
      Show detailed information for a specific task
      Example: view 1

  update <id> [--title <title>] [--description <desc>]
      Update task title and/or description
      Example: update 1 --title "New title"
      Example: update 1 --description "New description"
      Example: update 1 --title "Title" --description "Desc"

  delete <id>
      Permanently delete a task
      Example: delete 1

  complete <id>
      Mark a task as completed
      Example: complete 1

  uncomplete <id>
      Mark a task as incomplete
      Example: uncomplete 1

General:
  help
      Show this help message

  exit
      Exit the application (all data will be lost)

═══════════════════════════════════════════════════════════════
"""
