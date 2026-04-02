import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.notes import build_note_payload  # noqa: E402
from ai_news_assistant.rendering import render_note_markdown  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a structured note draft from a news item discussion."
    )
    parser.add_argument("--news-id", help="News item identifier.")
    parser.add_argument("--session-id", help="Reading session identifier.")
    parser.add_argument("--news-json", help="Inline JSON payload for a news item.")
    parser.add_argument("--session-json", help="Inline JSON payload for a discussion session.")
    parser.add_argument("--markdown-output", help="Optional path to write rendered markdown.")
    parser.add_argument(
        "--output",
        help="Optional path to write the note draft payload.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    news_item = json.loads(args.news_json) if args.news_json else {
        "title": args.news_id or "",
        "summary": "",
    }
    session = json.loads(args.session_json) if args.session_json else {
        "user_questions": [],
        "background_context": [],
        "discussion_flow": [],
        "final_insight": "",
        "content_angles": [],
        "original_user_thought_chain": [],
    }
    note_payload = build_note_payload(news_item, session)
    payload = {
        "news_id": args.news_id,
        "session_id": args.session_id,
        "template": "templates/deep_note.md",
        "note": note_payload,
        "markdown": render_note_markdown(note_payload),
        "todo": [
            "render note payload into the deep note template",
            "write the note to Feishu Docs",
            "update linked workflow state",
        ],
    }

    if args.output:
        Path(args.output).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    if args.markdown_output:
        Path(args.markdown_output).write_text(payload["markdown"], encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
