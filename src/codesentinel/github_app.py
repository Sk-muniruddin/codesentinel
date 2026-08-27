import os
import time
from pathlib import Path

import httpx
import jwt
from dotenv import load_dotenv


load_dotenv()


GITHUB_API_URL = "https://api.github.com"


def get_github_app_id() -> int:
    app_id = os.getenv("GITHUB_APP_ID")

    if not app_id:
        raise ValueError(
            "GITHUB_APP_ID environment variable is not set."
        )

    return int(app_id)


def get_github_app_private_key() -> str:
    key_path = os.getenv("GITHUB_APP_PRIVATE_KEY_PATH")

    if not key_path:
        raise ValueError(
            "GITHUB_APP_PRIVATE_KEY_PATH environment variable is not set."
        )

    path = Path(key_path)

    if not path.exists():
        raise FileNotFoundError(
            f"GitHub App private key not found: {path}"
        )

    return path.read_text(encoding="utf-8")


def create_github_app_jwt() -> str:
    app_id = get_github_app_id()
    private_key = get_github_app_private_key()

    now = int(time.time())

    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),
        "iss": str(app_id),
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
    )


def create_installation_access_token(
    installation_id: int,
) -> str:
    app_jwt = create_github_app_jwt()

    url = (
        f"{GITHUB_API_URL}/app/installations/"
        f"{installation_id}/access_tokens"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {app_jwt}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    response = httpx.post(
        url,
        headers=headers,
        timeout=30,
    )

    if response.status_code != 201:
        print("GitHub status:", response.status_code)
        print("GitHub response:", response.text)

    response.raise_for_status()

    return response.json()["token"]