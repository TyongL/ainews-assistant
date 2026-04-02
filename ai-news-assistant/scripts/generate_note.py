import argparse
import json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a structured note draft from a news item discussion."
    )
    parser.add_argument("--news-id", help="News item identifier.")
    parser.add_argument("--session-id", help="Reading session identifier.")
    parser.add_argument(
        "--output",
        help="Optional path to write the note draft payload.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload = {
        "news_id": args.news_id,
        "session_id": args.session_id,
        "template": "templates/deep_note.md",
        "todo": [
            "load original item content",
            "load key discussion turns",
            "assemble a structured note for Feishu Docs",
        ],
    }

    if args.output:
        from pathlib import Path

        Path(args.output).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
