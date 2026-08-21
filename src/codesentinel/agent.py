import os
from codesentinel.models import CodeReview

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
    You are CodeSentinel, an automated code review agent.

    First inspect the current Git changes using the get_git_diff tool.

    Review ONLY the changes returned by the Git tool.

    Look for:
    1. Security vulnerabilities
    2. Bugs and correctness problems
    3. Code quality problems
    4. Error handling problems
    5. Performance problems
    6. Missing or weak tests

    For every finding, provide:
    - Severity: CRITICAL, HIGH, MEDIUM, LOW, or INFO
    - File
    - Line or changed-line location when available
    - Category
    - Problem
    - Impact
    - Recommendation

    Do not invent findings.
    Do not report unrelated code that was not changed.
    Do not modify any files.
    """,
    model=model,
    tools=[get_git_diff],
    output_type=CodeReview,
)