import subprocess

from agents import function_tool


@function_tool
def get_git_diff() -> str:
    """Get all changes in the current Git repository compared with HEAD."""

    print(">>> get_git_diff() CALLED")

    result = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout