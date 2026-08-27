import httpx
from dotenv import load_dotenv

from codesentinel.github_app import create_installation_access_token


load_dotenv()


GITHUB_API_URL = "https://api.github.com"


def get_github_headers(
    installation_id: int,
) -> dict[str, str]:
    """Build headers using a GitHub App installation token."""

    token = create_installation_access_token(installation_id)

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_pull_request(
    owner: str,
    repository: str,
    pull_number: int,
    installation_id: int,
) -> dict:
    """Get information about a GitHub Pull Request."""

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/pulls/{pull_number}"
    )

    response = httpx.get(
        url,
        headers=get_github_headers(installation_id),
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()


def get_pull_request_diff(
    owner: str,
    repository: str,
    pull_number: int,
    installation_id: int,
) -> str:
    """Get the raw diff for a GitHub Pull Request."""

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/pulls/{pull_number}"
    )

    headers = get_github_headers(installation_id)
    headers["Accept"] = "application/vnd.github.v3.diff"

    response = httpx.get(
        url,
        headers=headers,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.text


def submit_pull_request_review(
    owner: str,
    repository: str,
    pull_number: int,
    event: str,
    body: str,
    installation_id: int,
) -> dict:
    """Submit a review to a GitHub Pull Request."""

    allowed_events = {
        "APPROVE",
        "REQUEST_CHANGES",
        "COMMENT",
    }

    event = event.upper()

    if event not in allowed_events:
        raise ValueError(
            f"Invalid review event: {event}. "
            f"Expected one of: {sorted(allowed_events)}"
        )

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/pulls/{pull_number}/reviews"
    )

    payload = {
        "event": event,
        "body": body,
    }

    response = httpx.post(
        url,
        headers=get_github_headers(installation_id),
        json=payload,
        timeout=30.0,
    )

    if response.is_error:
        print("GitHub status:", response.status_code)
        print("GitHub response:", response.text)

    response.raise_for_status()

    return response.json()