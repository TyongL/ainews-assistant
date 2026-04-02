import argparse
import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.feishu import (  # noqa: E402
    build_bitable_record_request,
    build_doc_create_request,
    build_tenant_access_token_request,
    load_feishu_settings,
    settings_summary,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Feishu sync CLI for AI News Assistant."
    )
    parser.add_argument(
        "--mode",
        choices=["check", "bitable", "doc"],
        default="check",
        help="Which Feishu request shape to prepare.",
    )
    parser.add_argument(
        "--fields-json",
        help="JSON object for Bitable fields when mode is bitable.",
    )
    parser.add_argument(
        "--title",
        default="AI资讯助手测试文档",
        help="Document title when mode is doc.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = load_feishu_settings(os.environ)

    if args.mode == "check":
        payload = {
            "mode": "check",
            "settings": settings_summary(settings),
            "auth_request": build_tenant_access_token_request(settings),
        }
    elif args.mode == "bitable":
        fields = json.loads(args.fields_json) if args.fields_json else {}
        payload = {
            "mode": "bitable",
            "settings": settings_summary(settings),
            "request": build_bitable_record_request(settings, fields),
        }
    else:
        payload = {
            "mode": "doc",
            "settings": settings_summary(settings),
            "request": build_doc_create_request(settings, args.title),
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
