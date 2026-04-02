import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.ingest import parse_news_input  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize raw AI news input into item-level records for later Feishu sync."
    )
    parser.add_argument(
        "--input-file",
        help="Path to a markdown or text file containing raw news input.",
    )
    parser.add_argument(
        "--text",
        help="Raw inline text for quick ingest testing.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write normalized placeholder output as JSON.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input_file and not args.text:
        parser.print_help()
        return 0

    source = "inline"
    raw_text = args.text or ""
    if args.input_file:
        raw_text = Path(args.input_file).read_text(encoding="utf-8")
        source = args.input_file

    parsed = parse_news_input(raw_text)
    payload = {
        "source": source,
        "raw_length": len(raw_text),
        "item_count": parsed["item_count"],
        "items": parsed["items"],
        "reading_list": parsed["reading_list"],
        "todo": [
            "enrich items with tags, dates, and source classification",
            "write results to Feishu Bitable and daily report doc",
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
