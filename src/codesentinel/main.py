import asyncio

from dotenv import load_dotenv

load_dotenv()

from agents import Runner

from codesentinel.agent import code_reviewer
from codesentinel.models import calculate_status


async def main():
    result = await Runner.run(
        code_reviewer,
        "Review the current Git changes in this repository.",
    )

    review = result.final_output

    review.overall_status = calculate_status(review.findings)

    print(review.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())