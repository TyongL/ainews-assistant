import argparse
import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.xhip_prompt import (  # noqa: E402
    DEFAULT_API_KEY_ENV,
    DEFAULT_API_URL,
    DEFAULT_CLIENT_ID_ENV,
    DEFAULT_KB_ID,
    DEFAULT_LOCAL_KB_DIR,
    build_kb_context,
    generate_xhip_prompt,
    load_url_or_content,
    load_xhip_resources,
    write_xhip_prompt_file,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成晓辉博士风格的视频脚本提示词。")
    parser.add_argument("--topic", required=True, help="视频脚本的主题")
    parser.add_argument("--content", help="直接文本内容")
    parser.add_argument("--content_file", help="本地文件路径（UTF-8 文本，如 .md/.txt）")
    parser.add_argument("--url", help="URL 参考资料")
    parser.add_argument("--kb_mode", default="auto", choices=["auto", "remote", "local", "off"])
    parser.add_argument("--kb_api_key", default=os.getenv(DEFAULT_API_KEY_ENV, ""))
    parser.add_argument("--kb_client_id", default=os.getenv(DEFAULT_CLIENT_ID_ENV, ""))
    parser.add_argument("--kb_api_url", default=DEFAULT_API_URL)
    parser.add_argument("--kb_id", default=DEFAULT_KB_ID)
    parser.add_argument("--kb_dir", default=str(DEFAULT_LOCAL_KB_DIR))
    parser.add_argument("--kb_timeout", type=int, default=30)
    parser.add_argument("--output", help="Optional JSON output path.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    user_content = load_url_or_content(args.url, args.content, args.content_file)
    logic, tone = load_xhip_resources(ROOT_DIR)
    kb_context = build_kb_context(
        args.topic,
        kb_mode=args.kb_mode,
        api_key=args.kb_api_key,
        client_id=args.kb_client_id,
        api_url=args.kb_api_url,
        kb_id=args.kb_id,
        kb_dir=Path(args.kb_dir),
        timeout_sec=args.kb_timeout,
    )
    prompt = generate_xhip_prompt(args.topic, kb_context, logic, tone, user_content)
    prompt_path = write_xhip_prompt_file(ROOT_DIR, prompt)

    payload = {
        "topic": args.topic,
        "kb_mode": args.kb_mode,
        "kb_context": kb_context,
        "prompt_file": str(prompt_path),
        "user_content_preview": user_content[:1000],
    }

    if args.output:
        Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
