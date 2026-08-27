import asyncio
import os

from dotenv import load_dotenv
from agents import Runner

from codesentinel.agent import code_reviewer
from codesentinel.diff_parser import parse_git_diff
from codesentinel.github_tools import get_pull_request_diff
from codesentinel.models import calculate_status


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"{name} environment variable is not set."
        )

    return value


async def main():
    # Temporary development configuration.
    # These values will later come dynamically from
    # the GitHub webhook event.
    owner = get_required_env("GITHUB_TEST_OWNER")
    repository = get_required_env("GITHUB_TEST_REPOSITORY")
    pull_number = int(get_required_env("GITHUB_TEST_PULL_NUMBER"))
    installation_id = int(
        get_required_env("GITHUB_TEST_INSTALLATION_ID")
    )

    # Get the raw diff from the GitHub Pull Request.
    diff = get_pull_request_diff(
        owner,
        repository,
        pull_number,
        installation_id,
    )

    # Parse the raw GitHub diff into structured changes.
    changes = parse_git_diff(diff)

    parsed_changes = "\n".join(
        f"{change.file}:{change.line} "
        f"[{change.change_type}] {change.content}"
        for change in changes
    )

    # Ask the Agent/LLM to review the changed code.
    result = await Runner.run(
        code_reviewer,
        f"""
Review the following parsed GitHub Pull Request changes.

IMPORTANT:
- Review only these changes.
- Do not review unrelated repository code.
- Treat the file and line information as authoritative.

PULL REQUEST:
{owner}/{repository}#{pull_number}

CHANGED CODE:
{parsed_changes}
""",
    )

    # The Agent already returned a CodeReview object.
    review = result.final_output

    # Python is the authoritative decision maker.
    final_status = calculate_status(review.findings)

    print("Findings:", review.findings)
    print("Summary:", review.summary)
    print("Final status:", final_status)


if __name__ == "__main__":
    asyncio.run(main())