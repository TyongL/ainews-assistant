import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.scripting import build_script_payload


class BuildScriptPayloadTests(unittest.TestCase):
    def test_extracts_topic_and_builds_publishable_payload(self) -> None:
        note = {
            "note_title": "系统级记忆与状态化 AI",
            "final_insight": "状态化 AI 的核心不是记得更多，而是记得可控。",
            "content_angles": [
                "为什么记忆功能越强，产品经理越要关注状态边界",
                "AI 产品的下半场不是更聪明，而是更可控",
            ],
            "original_user_thought_chain": [
                "我其实想知道，这到底算不算把复杂度甩给产品经理了？",
                "如果它只是会记，却不会忘，那不是更危险吗？",
            ],
        }

        payload = build_script_payload(note, script_type="short-video")

        self.assertEqual(payload["topic"], "系统级记忆与状态化 AI")
        self.assertIn("分享标题", payload)
        self.assertIn("引言摘要", payload)
        self.assertIn("口播稿正文", payload)
        self.assertIn("产品经理", payload["引言摘要"])

    def test_uses_original_user_tension_in_share_copy(self) -> None:
        note = {
            "note_title": "AI 记忆升级",
            "final_insight": "真正难的是状态可控，而不是记忆更强。",
            "content_angles": ["AI 记忆升级背后的状态管理问题"],
            "original_user_thought_chain": [
                "如果它只是会记，却不会忘，那不是更危险吗？"
            ],
        }

        payload = build_script_payload(note, script_type="short-video")

        self.assertIn("更危险", payload["引言摘要"])
        self.assertTrue(len(payload["分享标题"]) <= 20)

    def test_includes_xiaohui_style_script_sections(self) -> None:
        note = {
            "note_title": "异步 RL 框架 Slime",
            "final_insight": "关键不只是更快，而是把思考和执行拆开并行。",
            "content_angles": ["异步 RL 为什么像工厂流水线"],
            "original_user_thought_chain": [
                "这个东西是不是就像一个车间负责想，一个车间负责干？"
            ],
        }

        payload = build_script_payload(note, script_type="short-video")

        body = payload["口播稿正文"]
        self.assertIn("哈", body)
        self.assertIn("拜拜", body)
        self.assertIn("Title:", body)


if __name__ == "__main__":
    unittest.main()
