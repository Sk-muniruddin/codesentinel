import subprocess

from agents import function_tool


def _get_git_diff() -> str:

    print(">>> get_git_diff() CALLED")
    """Get all Git changes compared with HEAD."""

    result = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


def _get_changed_files() -> str:
    
    print(">>> get_changed_files() CALLED")
    """Get the list of files changed compared with HEAD."""

    result = subprocess.run(
        ["git", "diff", "HEAD", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


get_git_diff = function_tool(_get_git_diff)
get_changed_files = function_tool(_get_changed_files)