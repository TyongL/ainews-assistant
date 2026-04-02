from __future__ import annotations

import re
from typing import Any


LINK_PATTERN = re.compile(r"https?://\S+")
NUMBERED_ITEM_PATTERN = re.compile(r"^\s*(\d+)[\.\、]\s*(.+)$")


def _split_blocks(raw_text: str) -> list[str]:
    return [block.strip() for block in re.split(r"\n\s*\n", raw_text.strip()) if block.strip()]


def _normalize_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        match = NUMBERED_ITEM_PATTERN.match(line)
        if match:
            return match.group(2).strip()
    return lines[0] if lines else ""


def parse_news_input(raw_text: str) -> dict[str, Any]:
    blocks = _split_blocks(raw_text)
    items: list[dict[str, Any]] = []
    buffer: list[str] = []

    def flush_buffer() -> None:
        if not buffer:
            return
        block_text = "\n".join(buffer).strip()
        title = _normalize_title(block_text)
        links = LINK_PATTERN.findall(block_text)
        summary = title
        items.append(
            {
                "title": title,
                "summary": summary,
                "raw_text": block_text,
                "source_links": links,
            }
        )
        buffer.clear()

    for block in blocks:
        first_line = block.splitlines()[0].strip()
        if NUMBERED_ITEM_PATTERN.match(first_line) and buffer:
            flush_buffer()
        buffer.append(block)

    flush_buffer()

    reading_list = [
        {
            "index": index,
            "title": item["title"],
        }
        for index, item in enumerate(items, start=1)
    ]

    return {
        "item_count": len(items),
        "items": items,
        "reading_list": reading_list,
    }
