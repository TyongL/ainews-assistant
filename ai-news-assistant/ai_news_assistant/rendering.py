from __future__ import annotations

from typing import Any


def _render_list(value: Any) -> str:
    if isinstance(value, list):
        if not value:
            return ""
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def render_note_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# {payload.get('note_title', '')}",
            "",
            "## 原始资讯摘要",
            "",
            str(payload.get("source_summary", "")),
            "",
            "## 用户关注问题",
            "",
            _render_list(payload.get("user_questions", [])),
            "",
            "## 背景补充",
            "",
            _render_list(payload.get("background_context", [])),
            "",
            "## 讨论整理",
            "",
            _render_list(payload.get("discussion_flow", [])),
            "",
            "## 认知沉淀",
            "",
            str(payload.get("final_insight", "")),
            "",
            "## 可转创作观点",
            "",
            _render_list(payload.get("content_angles", [])),
            "",
            "## 全链路思考起点与原创原声",
            "",
            _render_list(payload.get("original_user_thought_chain", [])),
        ]
    )


def render_script_markdown(payload: dict[str, Any]) -> str:
    structure = payload.get("稿件结构概览", {})
    return "\n".join(
        [
            f"# {payload.get('topic', '')}",
            "",
            f"- 分享标题：{payload.get('分享标题', '')}",
            f"- 引言摘要：{payload.get('引言摘要', '')}",
            "",
            "## 知识库召回内容摘要",
            "",
            _render_list(payload.get("知识库召回内容摘要", [])),
            "",
            "## 口播稿正文",
            "",
            str(payload.get("口播稿正文", "")),
            "",
            "## 稿件结构概览",
            "",
            f"- Hook：{structure.get('hook', '')}",
            f"- Deep Dive：{structure.get('deep_dive', '')}",
            f"- Impact：{structure.get('impact', '')}",
        ]
    )
