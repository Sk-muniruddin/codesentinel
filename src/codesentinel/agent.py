import os

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)

from codesentinel.git_tools import get_git_diff


set_tracing_disabled(disabled=True)


client = AsyncOpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model="gemini-3.5-flash-lite",
    openai_client=client,
)


code_reviewer = Agent(
    name="CodeSentinel",
    instructions="""
    You are a code review agent.

    Review the current Git changes for:

    1. Bugs
    2. Security vulnerabilities
    3. Code quality problems
    4. Error handling problems
    5. Performance problems
    6. Missing or weak tests

    First inspect the Git diff using the available Git tool.

    Explain each finding clearly and provide a recommendation.

    Do not modify the code.
    """,
    model=model,
    tools=[get_git_diff],
)