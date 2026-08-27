from fastapi import FastAPI, Request

from agents import Runner

from codesentinel.agent import code_reviewer
from codesentinel.diff_parser import parse_git_diff
from codesentinel.github_models import PullRequestContext
from codesentinel.github_tools import get_pull_request_diff
from codesentinel.models import calculate_status


app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    # Ignore events that are not Pull Request events.
    if "pull_request" not in payload:
        return {
            "status": "ignored",
            "reason": "not a pull request event",
        }

    repository = payload["repository"]
    pull_request = payload["pull_request"]
    installation = payload.get("installation")

    if not installation:
        return {
            "status": "error",
            "reason": "installation information missing",
        }

    # Build dynamic Pull Request context from GitHub's event.
    context = PullRequestContext(
        owner=repository["owner"]["login"],
        repository=repository["name"],
        pull_number=pull_request["number"],
        action=payload["action"],
        installation_id=installation["id"],
    )

    print("Pull Request event received")
    print("Context:", context)

    # Only review PRs when they are opened or updated with new commits.
    if context.action not in {"opened", "reopened", "synchronize"}:
        return {
            "status": "ignored",
            "reason": f"action '{context.action}' does not trigger review",
        }

    # Get the PR diff using the GitHub App installation token.
    diff = get_pull_request_diff(
        context.owner,
        context.repository,
        context.pull_number,
        context.installation_id,
    )

    # Parse the GitHub diff.
    changes = parse_git_diff(diff)

    parsed_changes = "\n".join(
        f"{change.file}:{change.line} "
        f"[{change.change_type}] {change.content}"
        for change in changes
    )

    # Ask CodeSentinel's AI reviewer to review the changes.
    result = await Runner.run(
        code_reviewer,
        f"""
Review the following parsed GitHub Pull Request changes.

IMPORTANT:
- Review only these changes.
- Do not review unrelated repository code.
- Treat the file and line information as authoritative.

PULL REQUEST:
{context.owner}/{context.repository}#{context.pull_number}

CHANGED CODE:
{parsed_changes}
""",
    )

    # Agent returns the structured CodeReview object.
    review = result.final_output

    # Python remains the authoritative decision maker.
    final_status = calculate_status(review.findings)

    print("Findings:", review.findings)
    print("Summary:", review.summary)
    print("Final status:", final_status)

    return {
        "status": "reviewed",
        "owner": context.owner,
        "repository": context.repository,
        "pull_number": context.pull_number,
        "installation_id": context.installation_id,
        "review_status": final_status,
        "summary": review.summary,
        "findings_count": len(review.findings),
    }