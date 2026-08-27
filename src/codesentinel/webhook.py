from fastapi import FastAPI, Request
from agents import Runner

from codesentinel.agent import code_reviewer
from codesentinel.diff_parser import parse_git_diff
from codesentinel.github_models import PullRequestContext
from codesentinel.github_tools import (
    get_pull_request_diff,
    submit_pull_request_review,
)
from codesentinel.models import calculate_status


app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    # We only process Pull Request events.
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

    # Build dynamic Pull Request context from GitHub.
    context = PullRequestContext(
        owner=repository["owner"]["login"],
        repository=repository["name"],
        pull_number=pull_request["number"],
        action=payload["action"],
        installation_id=installation["id"],
    )

    print("Pull Request event received")
    print("Context:", context)

    # Only review when a PR is opened, reopened,
    # or new commits are pushed to the PR.
    if context.action not in {
        "opened",
        "reopened",
        "synchronize",
    }:
        return {
            "status": "ignored",
            "reason": (
                f"action '{context.action}' "
                "does not trigger review"
            ),
        }

    # Get the PR diff using the GitHub App installation token.
    diff = get_pull_request_diff(
        owner=context.owner,
        repository=context.repository,
        pull_number=context.pull_number,
        installation_id=context.installation_id,
    )

    # Parse the GitHub diff.
    changes = parse_git_diff(diff)

    parsed_changes = "\n".join(
        f"{change.file}:{change.line} "
        f"[{change.change_type}] {change.content}"
        for change in changes
    )

    # Send the changed code to the AI reviewer.
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

    # The Agent returns the structured CodeReview object.
    review = result.final_output

    # Python remains the authoritative decision maker.
    final_status = calculate_status(review.findings)

    print("Findings:", review.findings)
    print("Summary:", review.summary)
    print("Final status:", final_status)

    # Convert our internal status into a GitHub review event.
    if final_status == "CHANGES_REQUESTED":
        review_event = "REQUEST_CHANGES"
    else:
        review_event = "APPROVE"

    # Build the review message that will appear on GitHub.
    review_body = f"""## CodeSentinel Review

**Status:** {final_status}

### Summary

{review.summary}
"""

    if review.findings:
        review_body += "\n### Findings\n\n"

        for finding in review.findings:
            review_body += (
                f"- **{finding.severity}** — "
                f"`{finding.file}:{finding.line}`\n"
                f"  - **Category:** {finding.category}\n"
                f"  - **Problem:** {finding.problem}\n"
                f"  - **Impact:** {finding.impact}\n"
                f"  - **Recommendation:** "
                f"{finding.recommendation}\n\n"
            )

    # Submit the AI review to the GitHub Pull Request.
    github_review = submit_pull_request_review(
        owner=context.owner,
        repository=context.repository,
        pull_number=context.pull_number,
        event=review_event,
        body=review_body,
        installation_id=context.installation_id,
    )

    print(
        "GitHub review submitted:",
        github_review.get("id"),
    )

    return {
        "status": "reviewed",
        "owner": context.owner,
        "repository": context.repository,
        "pull_number": context.pull_number,
        "installation_id": context.installation_id,
        "review_status": final_status,
        "github_review_event": review_event,
        "summary": review.summary,
        "findings_count": len(review.findings),
    }