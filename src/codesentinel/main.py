import asyncio
from dotenv import load_dotenv

load_dotenv()

from agents import Runner
from codesentinel.agent import code_reviewer

async def main():
    code = """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id=" + user_id
    return db.execute(query)
"""

    result = await Runner.run(
        code_reviewer,
        f"Review this code:\n\n{code}"
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())