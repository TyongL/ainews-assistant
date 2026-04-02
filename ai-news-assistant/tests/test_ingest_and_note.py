import json
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.ingest import parse_news_input
from ai_news_assistant.notes import build_note_payload


class ParseNewsInputTests(unittest.TestCase):
    def test_splits_numbered_items_and_preserves_links(self) -> None:
        raw_text = """
1. OpenAI 发布了新的记忆能力更新，争议点在于连续性提升和状态污染风险。
https://example.com/openai-memory

2. 某大模型团队发布了新的多模态模型，强调更低推理成本和更强文档理解。
https://example.com/multimodal
""".strip()

        parsed = parse_news_input(raw_text)

        self.assertEqual(len(parsed["items"]), 2)
        self.assertEqual(parsed["items"][0]["source_links"], ["https://example.com/openai-memory"])
        self.assertEqual(parsed["items"][1]["source_links"], ["https://example.com/multimodal"])
        self.assertEqual(parsed["reading_list"][0]["index"], 1)
        self.assertEqual(parsed["reading_list"][1]["index"], 2)

    def test_creates_ordered_reading_list_titles(self) -> None:
        raw_text = """
1. 这是一条关于 Agent 经济的新资讯，讨论企业应用落地。
https://example.com/agent
""".strip()

        parsed = parse_news_input(raw_text)

        self.assertEqual(parsed["reading_list"], [{"index": 1, "title": "这是一条关于 Agent 经济的新资讯，讨论企业应用落地。"}])


class BuildNotePayloadTests(unittest.TestCase):
    def test_preserves_original_thought_chain_in_note_payload(self) -> None:
        news_item = {
            "title": "系统级记忆与状态化 AI",
            "summary": "围绕系统记忆能力和状态管理风险的资讯。",
        }
        session = {
            "user_questions": [
                "这到底是体验升级还是工程复杂度转移？",
                "如果它记错了，后面是不是会越来越脏？",
            ],
            "background_context": [
                "长期记忆系统的关键在于作用域、更新条件和撤销机制。"
            ],
            "discussion_flow": [
                "讨论从功能体验推进到状态边界和系统控制问题。"
            ],
            "final_insight": "状态化 AI 的核心不是记得更多，而是记得可控。",
            "content_angles": [
                "为什么记忆功能越强，产品经理越要关注状态边界"
            ],
            "original_user_thought_chain": [
                "我其实想知道，这到底算不算把复杂度甩给产品经理了？",
                "如果它只是会记，却不会忘，那不是更危险吗？",
            ],
        }

        payload = build_note_payload(news_item, session)

        self.assertEqual(payload["note_title"], "系统级记忆与状态化 AI")
        self.assertIn("original_user_thought_chain", payload)
        self.assertEqual(len(payload["original_user_thought_chain"]), 2)
        self.assertIn("复杂度甩给产品经理", payload["original_user_thought_chain"][0])


if __name__ == "__main__":
    unittest.main()
