import asyncio

from dotenv import load_dotenv

load_dotenv()

from agents import Runner

from codesentinel.agent import code_reviewer


async def main():
    result = await Runner.run(
        code_reviewer,
        "Review the current Git changes in this repository.",
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())