from __future__ import annotations

import re
from typing import Any


MARKDOWN_LINK_PATTERN = re.compile(r"\[阅读原文\]\((https?://[^\)]+)\)")


def build_fetch_plan(news_item: dict[str, Any], user_message: str) -> dict[str, Any]:
    raw_text = news_item.get("raw_text", "")
    links = news_item.get("source_links", [])
    markdown_links = MARKDOWN_LINK_PATTERN.findall(raw_text)
    combined_links = markdown_links + [link for link in links if link not in markdown_links]
    primary_url = combined_links[0] if combined_links else None

    return {
        "strategy": "source_link_first",
        "primary_url": primary_url,
        "fallback": "fresh_search_if_source_insufficient",
        "should_store_as_new_resource": False,
        "user_message": user_message,
    }
