import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.scripting import build_script_payload  # noqa: E402
from ai_news_assistant.rendering import render_script_markdown  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a script-ready draft from a structured note."
    )
    parser.add_argument("--note-id", help="Structured note identifier.")
    parser.add_argument("--note-json", help="Inline JSON payload for a structured note.")
    parser.add_argument(
        "--script-type",
        default="short-video",
        help="Script type to generate, for example short-video or summary-post.",
    )
    parser.add_argument("--markdown-output", help="Optional path to write rendered markdown.")
    parser.add_argument(
        "--output",
        help="Optional path to write the script payload.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    note = json.loads(args.note_json) if args.note_json else {
        "note_title": args.note_id or "AI资讯主题",
        "final_insight": "",
        "content_angles": [],
        "original_user_thought_chain": [],
    }
    script_payload = build_script_payload(note, args.script_type)
    payload = {
        "note_id": args.note_id,
        "script_type": args.script_type,
        "template": "templates/script.md",
        "script": script_payload,
        "markdown": render_script_markdown(script_payload),
        "todo": [
            "merge note content with XHIP-style persona and structure",
            "write final result to a Feishu doc and update workflow state",
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
