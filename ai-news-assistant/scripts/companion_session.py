import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.companion import build_companion_plan  # noqa: E402
from ai_news_assistant.sessions import append_session_turn  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a source-first discussion plan for one AI news item."
    )
    parser.add_argument("--news-json", required=True, help="JSON payload for the selected news item.")
    parser.add_argument("--message", required=True, help="User message about the selected item.")
    parser.add_argument(
        "--unfamiliar-terms-json",
        help="Optional JSON array of unfamiliar terms that require fresh research.",
    )
    parser.add_argument("--session-file", help="Optional path to persist the discussion draft.")
    parser.add_argument("--output", help="Optional file path for writing the session plan.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    news_item = json.loads(args.news_json)
    unfamiliar_terms = json.loads(args.unfamiliar_terms_json) if args.unfamiliar_terms_json else []
    plan = build_companion_plan(news_item, args.message, unfamiliar_terms)

    if args.session_file:
        append_session_turn(
            Path(args.session_file),
            role="user",
            content=args.message,
            preserve_as_original_thought=True,
        )

    payload = {
        "news_title": news_item.get("title", ""),
        "session_plan": plan,
        "todo": [
            "use the selected news item as ground truth",
            "fetch fresh background only when the source is insufficient or terms are unfamiliar",
            "accumulate a hidden cognitive draft for later note generation",
        ],
    }

    if args.output:
        Path(args.output).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
