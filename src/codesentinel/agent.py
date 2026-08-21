from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)
import os

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-3.7-flash",
    openai_client=client,
)

code_reviewer = Agent(
    name="CodeSentinel",
    instructions="""
    You are a code review agent.

    Review the provided code for:
    1. Bugs
    2. Security vulnerabilities
    3. Code quality problems
    4. Error handling problems
    5. Performance problems
    6. Missing or weak tests

    Explain each finding clearly and provide a recommendation.
    Do not modify the code.
    """,
    model=model,
)