import asyncio

from dotenv import load_dotenv
from agents import Runner

from codesentinel.agent import code_reviewer
from codesentinel.diff_parser import parse_git_diff
from codesentinel.github_tools import get_pull_request_diff
from codesentinel.models import calculate_status


load_dotenv()


OWNER = "Sk-muniruddin"
REPOSITORY = "codesentinel"
PULL_NUMBER = 1


async def main():
    # Get the raw diff from the GitHub Pull Request.
    diff = get_pull_request_diff(
        OWNER,
        REPOSITORY,
        PULL_NUMBER,
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
{OWNER}/{REPOSITORY}#{PULL_NUMBER}

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