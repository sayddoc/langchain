"""GitHub data retrieval tools."""

from __future__ import annotations

from typing import Any

import requests
from langchain_core.tools import tool


@tool
def github_repo_summary(owner: str, repo: str) -> dict[str, Any]:
    """Fetch metadata for a public GitHub repository.

    Args:
        owner: Repository owner.
        repo: Repository name.

    Returns:
        Repository metadata.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    payload = response.json()
    return {
        "full_name": payload.get("full_name"),
        "description": payload.get("description"),
        "stars": payload.get("stargazers_count", 0),
        "forks": payload.get("forks_count", 0),
        "open_issues": payload.get("open_issues_count", 0),
        "updated_at": payload.get("updated_at"),
        "url": payload.get("html_url"),
    }


@tool
def github_recent_issues(owner: str, repo: str, limit: int = 5) -> list[dict[str, Any]]:
    """Fetch recent open issues for a public repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(url, params={"state": "open", "per_page": limit}, timeout=10)
    response.raise_for_status()
    payload = response.json()
    return [
        {
            "title": issue.get("title", ""),
            "number": issue.get("number"),
            "url": issue.get("html_url", ""),
        }
        for issue in payload
        if "pull_request" not in issue
    ]
