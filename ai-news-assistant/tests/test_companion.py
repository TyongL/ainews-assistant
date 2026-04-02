import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.companion import build_companion_plan


class BuildCompanionPlanTests(unittest.TestCase):
    def test_uses_source_as_ground_truth_and_marks_background_as_optional(self) -> None:
        news_item = {
            "title": "系统级记忆与状态化 AI",
            "summary": "这条资讯讨论 AI 记忆能力升级带来的连续性体验和状态污染风险。",
            "raw_text": (
                "OpenAI 推出新的记忆机制，用户体验更连续，但也让状态污染风险更值得关注。"
            ),
            "source_links": ["https://example.com/openai-memory"],
        }

        plan = build_companion_plan(
            news_item=news_item,
            user_message="这到底是体验升级还是工程复杂度转移？",
            unfamiliar_terms=[],
        )

        self.assertEqual(plan["source_priority"], "ground_truth_first")
        self.assertFalse(plan["needs_fresh_research"])
        self.assertIn("体验升级还是工程复杂度转移", plan["discussion_focus"])
        self.assertEqual(plan["source_links"], ["https://example.com/openai-memory"])

    def test_flags_unfamiliar_terms_for_fresh_research_instead_of_guessing(self) -> None:
        news_item = {
            "title": "神秘新芯片",
            "summary": "文章提到一种新芯片方案，但没有详细展开。",
            "raw_text": "某团队发布了代号 X-QuantumStack 的新芯片架构。",
            "source_links": [],
        }

        plan = build_companion_plan(
            news_item=news_item,
            user_message="这个 X-QuantumStack 到底是什么？",
            unfamiliar_terms=["X-QuantumStack"],
        )

        self.assertTrue(plan["needs_fresh_research"])
        self.assertIn("X-QuantumStack", plan["unknown_terms"])
        self.assertIn("instead of guessing", plan["research_reason"])

    def test_requires_plain_language_explanation_for_technical_terms(self) -> None:
        news_item = {
            "title": "异步 RL 框架",
            "summary": "文章提到了异步 RL 框架 Slime。",
            "raw_text": "提出异步 RL 框架 Slime。",
            "source_links": [],
        }

        plan = build_companion_plan(
            news_item=news_item,
            user_message="异步 RL 到底什么意思？",
            unfamiliar_terms=[],
        )

        self.assertTrue(plan["plain_language_required"])


if __name__ == "__main__":
    unittest.main()
