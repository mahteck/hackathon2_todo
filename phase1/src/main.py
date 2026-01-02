"""
Main CLI application entry point.

Handles user interaction loop, command routing, and display.
"""
from src.task_service import TaskService
from src.task_repository import TaskRepository
from src.command_parser import parse_command, is_valid_command
from src.cli_formatter import (
    format_welcome, format_goodbye, format_help,
    format_success, format_error,
    format_task_list, format_task_detail
)
from src.exceptions import TodoAppError


def handle_add(args: list[str], service: TaskService) -> None:
    """
    Handle 'add' command to create a new task.

    Args:
        args: Command arguments [title, description (optional)]
        service: TaskService instance
    """
    if not args:
        print(format_error("Missing required argument: title"))
        return

    title = args[0]
    description = args[1] if len(args) > 1 else ""

    task = service.add_task(title, description)
    print(format_success("Task created successfully"))
    print(f"  ID: {task['id']}")
    print(f"  Title: {task['title']}")
    if task['description']:
        print(f"  Description: {task['description']}")
    print(f"  Status: Incomplete")


def handle_list(service: TaskService) -> None:
    """
    Handle 'list' command to show all tasks.

    Args:
        service: TaskService instance
    """
    tasks = service.get_all_tasks()
    print(format_task_list(tasks))


def handle_view(args: list[str], service: TaskService) -> None:
    """
    Handle 'view' command to show task details.

    Args:
        args: Command arguments [task_id]
        service: TaskService instance
    """
    if not args:
        print(format_error("Missing required argument: task ID"))
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print(format_error("Invalid task ID: must be a positive integer"))
        return

    task = service.get_task_by_id(task_id)
    print(format_task_detail(task))


def handle_update(args: list[str], flags: dict[str, str], service: TaskService) -> None:
    """
    Handle 'update' command to modify a task.

    Args:
        args: Command arguments [task_id]
        flags: Flag dictionary with 'title' and/or 'description'
        service: TaskService instance
    """
    if not args:
        print(format_error("Missing required argument: task ID"))
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print(format_error("Invalid task ID: must be a positive integer"))
        return

    title = flags.get("title")
    description = flags.get("description")

    task = service.update_task(task_id, title=title, description=description)
    print(format_success("Task updated successfully"))
    print(f"  ID: {task['id']}")
    print(f"  Title: {task['title']}")
    if description is not None:
        print(f"  Description: {task['description']}")


def handle_delete(args: list[str], service: TaskService) -> None:
    """
    Handle 'delete' command to remove a task.

    Args:
        args: Command arguments [task_id]
        service: TaskService instance
    """
    if not args:
        print(format_error("Missing required argument: task ID"))
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print(format_error("Invalid task ID: must be a positive integer"))
        return

    deleted_task = service.delete_task(task_id)
    print(format_success("Task deleted successfully"))
    print(f"  Deleted task #{deleted_task['id']}: \"{deleted_task['title']}\"")


def handle_complete(args: list[str], service: TaskService) -> None:
    """
    Handle 'complete' command to mark task as done.

    Args:
        args: Command arguments [task_id]
        service: TaskService instance
    """
    if not args:
        print(format_error("Missing required argument: task ID"))
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print(format_error("Invalid task ID: must be a positive integer"))
        return

    task = service.complete_task(task_id)
    print(format_success("Task marked as complete"))
    print(f"  Task #{task['id']}: \"{task['title']}\" ✓")


def handle_uncomplete(args: list[str], service: TaskService) -> None:
    """
    Handle 'uncomplete' command to mark task as not done.

    Args:
        args: Command arguments [task_id]
        service: TaskService instance
    """
    if not args:
        print(format_error("Missing required argument: task ID"))
        return

    try:
        task_id = int(args[0])
    except ValueError:
        print(format_error("Invalid task ID: must be a positive integer"))
        return

    task = service.uncomplete_task(task_id)
    print(format_success("Task marked as incomplete"))
    print(f"  Task #{task['id']}: \"{task['title']}\" [ ]")


def handle_help() -> None:
    """Handle 'help' command to show usage information."""
    print(format_help())


def main() -> None:
    """Main application loop."""
    repository = TaskRepository()
    service = TaskService(repository)

    print(format_welcome())

    while True:
        try:
            user_input = input("> ").strip()

            if not user_input:
                continue

            command, args, flags = parse_command(user_input)

            if command == "exit":
                print(format_goodbye())
                break

            if not is_valid_command(command):
                print(format_error(f"Unknown command '{command}'. Type 'help' for available commands."))
                continue

            # Route to appropriate handler
            if command == "add":
                handle_add(args, service)
            elif command == "list":
                handle_list(service)
            elif command == "view":
                handle_view(args, service)
            elif command == "update":
                handle_update(args, flags, service)
            elif command == "delete":
                handle_delete(args, service)
            elif command == "complete":
                handle_complete(args, service)
            elif command == "uncomplete":
                handle_uncomplete(args, service)
            elif command == "help":
                handle_help()

        except TodoAppError as e:
            print(format_error(str(e)))
        except KeyboardInterrupt:
            print("\n" + format_goodbye())
            break
        except Exception as e:
            print(format_error(f"An unexpected error occurred: {e}"))


if __name__ == "__main__":
    main()
