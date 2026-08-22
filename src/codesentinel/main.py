import asyncio

from dotenv import load_dotenv

load_dotenv()

from agents import Runner

from codesentinel.agent import code_reviewer
from codesentinel.git_tools import _get_parsed_changes
from codesentinel.models import calculate_status


async def main():
    changes = _get_parsed_changes()

    result = await Runner.run(
        code_reviewer,
        f"""
Review the following parsed Git changes.

IMPORTANT:
- Review only these changes.
- Do not review unrelated repository code.
- Treat the file and line information as authoritative.

CHANGED CODE:
{changes}
""",
    )

    review = result.final_output

    review.overall_status = calculate_status(review.findings)

    print(review.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())