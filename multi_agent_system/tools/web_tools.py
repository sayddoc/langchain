"""Web-oriented tools used by the Research Agent."""

from __future__ import annotations

from typing import Any

import requests
from langchain_core.tools import tool


@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web through DuckDuckGo instant answer API.

    Args:
        query: Search query.

    Returns:
        JSON-like object containing search snippets and references.
    """
    response = requests.get(
        "https://api.duckduckgo.com/",
        params={"q": query, "format": "json", "no_html": 1},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    related = payload.get("RelatedTopics", [])
    snippets = []
    for item in related[:5]:
        if isinstance(item, dict) and item.get("Text"):
            snippets.append({"text": item["Text"], "url": item.get("FirstURL", "")})

    return {
        "abstract": payload.get("AbstractText", ""),
        "heading": payload.get("Heading", ""),
        "snippets": snippets,
    }


@tool
def http_get_json(url: str) -> dict[str, Any]:
    """Fetch generic JSON data from an HTTP endpoint.

    Args:
        url: HTTP/HTTPS endpoint.

    Returns:
        Parsed JSON payload.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
