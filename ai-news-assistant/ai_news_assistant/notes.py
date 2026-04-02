from __future__ import annotations

from typing import Any


def build_note_payload(news_item: dict[str, Any], session: dict[str, Any]) -> dict[str, Any]:
    return {
        "note_title": news_item.get("title", ""),
        "source_summary": news_item.get("summary", ""),
        "user_questions": session.get("user_questions", []),
        "background_context": session.get("background_context", []),
        "discussion_flow": session.get("discussion_flow", []),
        "final_insight": session.get("final_insight", ""),
        "content_angles": session.get("content_angles", []),
        "original_user_thought_chain": session.get("original_user_thought_chain", []),
    }
