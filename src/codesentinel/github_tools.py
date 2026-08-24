import os

import httpx
from dotenv import load_dotenv


load_dotenv()


GITHUB_API_URL = "https://api.github.com"


def get_github_token() -> str:
    """Get the GitHub token from the environment."""

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set.")

    return token


def get_github_headers() -> dict[str, str]:
    """Build headers required for GitHub API requests."""

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {get_github_token()}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_pull_request(
    owner: str,
    repository: str,
    pull_number: int,
) -> dict:
    """Get information about a GitHub Pull Request."""

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/pulls/{pull_number}"
    )

    response = httpx.get(
        url,
        headers=get_github_headers(),
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()


def get_pull_request_diff(
    owner: str,
    repository: str,
    pull_number: int,
) -> str:
    """Get the raw diff for a GitHub Pull Request."""

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repository}/pulls/{pull_number}"
    )

    headers = get_github_headers()
    headers["Accept"] = "application/vnd.github.v3.diff"

    response = httpx.get(
        url,
        headers=headers,
        timeout=30.0,
    )

    response.raise_for_status()

    return response.text