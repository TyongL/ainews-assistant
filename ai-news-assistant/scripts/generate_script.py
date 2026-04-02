import argparse
import json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a script-ready draft from a structured note."
    )
    parser.add_argument("--note-id", help="Structured note identifier.")
    parser.add_argument(
        "--script-type",
        default="short-video",
        help="Script type to generate, for example short-video or summary-post.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the script payload.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload = {
        "note_id": args.note_id,
        "script_type": args.script_type,
        "template": "templates/script.md",
        "todo": [
            "load note content",
            "apply script prompt and style rules",
            "write final result to a Feishu doc and update workflow state",
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
