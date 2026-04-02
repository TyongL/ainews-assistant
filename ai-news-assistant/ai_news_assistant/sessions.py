from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_session_draft(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "turns": [],
            "original_user_thought_chain": [],
        }
    return json.loads(path.read_text(encoding="utf-8"))


def append_session_turn(
    path: Path,
    role: str,
    content: str,
    preserve_as_original_thought: bool = False,
) -> dict[str, Any]:
    draft = load_session_draft(path)
    draft["turns"].append({"role": role, "content": content})
    if role == "user" and preserve_as_original_thought:
        draft["original_user_thought_chain"].append(content)
    path.write_text(json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8")
    return draft
