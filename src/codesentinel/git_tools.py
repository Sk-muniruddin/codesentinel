import subprocess

from agents import function_tool

from codesentinel.diff_parser import parse_git_diff


def _get_git_diff() -> str:
    """Get all Git changes compared with HEAD."""

    print(">>> get_git_diff() CALLED")

    result = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


def _get_changed_files() -> str:
    """Get the list of files changed compared with HEAD."""

    result = subprocess.run(
        ["git", "diff", "HEAD", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


def _get_parsed_changes() -> str:
    """Get meaningful changed lines from the current Git diff."""

    diff = _get_git_diff()

    changes = parse_git_diff(diff)

    return "\n".join(
        f"{change.file}:{change.line} "
        f"[{change.change_type}] {change.content}"
        for change in changes
    )


get_git_diff = function_tool(_get_git_diff)
get_changed_files = function_tool(_get_changed_files)