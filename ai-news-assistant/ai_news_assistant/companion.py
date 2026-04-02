from __future__ import annotations

import re
from typing import Any


TECHNICAL_TERM_PATTERNS = [
    re.compile(r"\bRL\b", re.IGNORECASE),
    re.compile(r"\bMoE\b", re.IGNORECASE),
    re.compile(r"\bDPO\b", re.IGNORECASE),
    re.compile(r"\bScaling Law\b", re.IGNORECASE),
]


def _requires_plain_language(text: str) -> bool:
    return any(pattern.search(text) for pattern in TECHNICAL_TERM_PATTERNS)


def build_companion_plan(
    news_item: dict[str, Any],
    user_message: str,
    unfamiliar_terms: list[str] | None = None,
) -> dict[str, Any]:
    unfamiliar_terms = unfamiliar_terms or []
    combined_text = " ".join(
        [
            news_item.get("title", ""),
            news_item.get("summary", ""),
            news_item.get("raw_text", ""),
            user_message,
        ]
    )

    needs_fresh_research = len(unfamiliar_terms) > 0
    research_reason = (
        f"Need fresh research for unfamiliar terms {', '.join(unfamiliar_terms)} instead of guessing."
        if needs_fresh_research
        else ""
    )

    return {
        "source_priority": "ground_truth_first",
        "discussion_focus": user_message,
        "source_links": news_item.get("source_links", []),
        "needs_fresh_research": needs_fresh_research,
        "unknown_terms": unfamiliar_terms,
        "research_reason": research_reason,
        "plain_language_required": _requires_plain_language(combined_text),
        "keep_hidden_cognitive_draft": True,
        "challenge_flawed_reasoning": True,
    }
