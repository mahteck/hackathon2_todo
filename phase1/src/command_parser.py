"""
Command-line input parsing utilities.

Parses user input into command name, arguments, and flags.
"""
import shlex
from typing import Tuple


# Valid command names
VALID_COMMANDS = [
    "add", "list", "view", "update", "delete",
    "complete", "uncomplete", "help", "exit"
]


def parse_command(input_str: str) -> Tuple[str, list[str], dict[str, str]]:
    """
    Parse command input into components.

    Args:
        input_str: Raw user input

    Returns:
        Tuple of (command_name, args, flags)
        - command_name: Lowercased command (e.g., "add")
        - args: Positional arguments (e.g., ["1", "Buy milk"])
        - flags: Flag dictionary (e.g., {"title": "New Title"})

    Examples:
        >>> parse_command("add Buy milk")
        ("add", ["Buy", "milk"], {})

        >>> parse_command('add "Buy milk" "From store"')
        ("add", ["Buy milk", "From store"], {})

        >>> parse_command("update 1 --title New Title")
        ("update", ["1"], {"title": "New Title"})
    """
    if not input_str.strip():
        return ("", [], {})

    # Use shlex to handle quoted strings properly
    try:
        tokens = shlex.split(input_str)
    except ValueError:
        # If shlex fails (e.g., unmatched quotes), fall back to simple split
        tokens = input_str.split()

    if not tokens:
        return ("", [], {})

    # First token is the command
    command = tokens[0].lower()

    # Parse remaining tokens for args and flags
    args = []
    flags = {}
    i = 1

    while i < len(tokens):
        token = tokens[i]

        # Check if token is a flag (starts with --)
        if token.startswith("--"):
            flag_name = token[2:]  # Remove --

            # Get flag value (next token)
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                flag_value = tokens[i + 1]
                flags[flag_name] = flag_value
                i += 2  # Skip both flag and value
            else:
                # Flag without value, skip it
                i += 1
        else:
            # Regular argument
            args.append(token)
            i += 1

    return (command, args, flags)


def is_valid_command(command: str) -> bool:
    """
    Check if command name is valid.

    Args:
        command: Command name to validate

    Returns:
        True if valid, False otherwise
    """
    return command.lower() in VALID_COMMANDS
