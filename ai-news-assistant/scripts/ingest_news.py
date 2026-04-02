import argparse
import json
from pathlib import Path


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

    payload = {
        "source": source,
        "raw_length": len(raw_text),
        "todo": [
            "split raw input into item-level news units",
            "extract title, summary, links, tags, and dates",
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
