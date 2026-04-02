import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.fetching import build_fetch_plan
from ai_news_assistant.rendering import render_note_markdown, render_script_markdown
from ai_news_assistant.sessions import append_session_turn, load_session_draft


class BuildFetchPlanTests(unittest.TestCase):
    def test_extracts_followup_link_and_prefers_source_link(self) -> None:
        news_item = {
            "title": "记忆更新",
            "summary": "提到了新记忆机制。",
            "raw_text": "OpenAI 推出新的记忆机制。[阅读原文](https://example.com/full-article)",
            "source_links": ["https://example.com/full-article"],
        }

        plan = build_fetch_plan(news_item, "这个机制细节到底是什么？")

        self.assertEqual(plan["primary_url"], "https://example.com/full-article")
        self.assertEqual(plan["strategy"], "source_link_first")
        self.assertFalse(plan["should_store_as_new_resource"])


class SessionDraftTests(unittest.TestCase):
    def test_appends_turns_and_persists_original_user_thought_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            session_file = Path(temp_dir) / "session.json"

            append_session_turn(
                session_file,
                role="user",
                content="这到底算不算把复杂度甩给产品经理了？",
                preserve_as_original_thought=True,
            )
            append_session_turn(
                session_file,
                role="assistant",
                content="关键不是记忆更强，而是状态边界怎么控住。",
            )

            draft = load_session_draft(session_file)

            self.assertEqual(len(draft["turns"]), 2)
            self.assertEqual(len(draft["original_user_thought_chain"]), 1)
            self.assertIn("复杂度甩给产品经理", draft["original_user_thought_chain"][0])


class RenderMarkdownTests(unittest.TestCase):
    def test_renders_note_markdown_with_original_thought_chain(self) -> None:
        payload = {
            "note_title": "系统级记忆与状态化 AI",
            "source_summary": "围绕系统记忆能力和状态管理风险的资讯。",
            "user_questions": ["这到底是体验升级还是工程复杂度转移？"],
            "background_context": ["长期记忆系统的关键在于作用域和撤销机制。"],
            "discussion_flow": ["讨论从体验推进到状态边界。"],
            "final_insight": "状态化 AI 的核心不是记得更多，而是记得可控。",
            "content_angles": ["为什么记忆功能越强，产品经理越要关注状态边界"],
            "original_user_thought_chain": ["如果它只是会记，却不会忘，那不是更危险吗？"],
        }

        markdown = render_note_markdown(payload)

        self.assertIn("## 全链路思考起点与原创原声", markdown)
        self.assertIn("更危险", markdown)

    def test_renders_script_markdown_with_titles_and_body(self) -> None:
        payload = {
            "topic": "系统级记忆与状态化 AI",
            "分享标题": "记忆升级背后的状态问题",
            "引言摘要": "这不是简单升级，而是状态管理上台面。",
            "口播稿正文": "Title: 系统级记忆与状态化 AI\n\n哈，大家好。\n\n正文。\n\n拜拜",
            "稿件结构概览": {
                "hook": "冲突开场",
                "deep_dive": "深入拆解",
                "impact": "行业影响",
            },
        }

        markdown = render_script_markdown(payload)

        self.assertIn("# 系统级记忆与状态化 AI", markdown)
        self.assertIn("记忆升级背后的状态问题", markdown)
        self.assertIn("拜拜", markdown)


if __name__ == "__main__":
    unittest.main()
