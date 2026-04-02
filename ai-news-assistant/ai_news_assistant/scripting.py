from __future__ import annotations

from typing import Any


def _extract_topic(note: dict[str, Any]) -> str:
    return note.get("note_title") or "AI资讯主题"


def _build_share_title(topic: str, angle: str) -> str:
    base = angle or topic
    compact = base.replace("为什么", "").replace("，", "").replace("。", "")
    return compact[:20]


def _build_intro(note: dict[str, Any]) -> str:
    original_chain = note.get("original_user_thought_chain", [])
    tension = original_chain[0] if original_chain else "很多人以为这只是功能升级。"
    final_insight = note.get("final_insight", "")
    intro = (
        f"作为一线做 AI 产品的人，看到这个话题真的很容易被击中：{tension}"
        f" 乍一看像能力升级，往深处看其实是系统状态管理的问题。{final_insight}"
    )
    return intro[:120]


def _build_body(topic: str, note: dict[str, Any]) -> str:
    final_insight = note.get("final_insight", "")
    angles = note.get("content_angles", [])
    angle_text = angles[0] if angles else topic
    return (
        f"Title: {topic[:20]}\n\n"
        f"哈，大家好，今天想聊一个让我心情很复杂但又很兴奋的话题，叫 {topic}。\n\n"
        f"很多人看到这个现象，第一反应是功能更强了，是吧。但我更关心的是，它背后的系统到底怎么控住。"
        f"这有点像一个工厂流水线，一个车间负责想，一个车间负责干，如果中间状态传脏了，后面全线都会乱。\n\n"
        f"{angle_text}。{final_insight}\n\n"
        f"所以这件事最值得看的，不只是模型又强了一点，而是产品和系统设计是不是跟上了。拜拜"
    )


def build_script_payload(note: dict[str, Any], script_type: str) -> dict[str, Any]:
    topic = _extract_topic(note)
    angles = note.get("content_angles", [])
    primary_angle = angles[0] if angles else topic

    return {
        "topic": topic,
        "script_type": script_type,
        "分享标题": _build_share_title(topic, primary_angle),
        "引言摘要": _build_intro(note),
        "知识库召回内容摘要": [
            "待接入远程知识库召回",
            "待融合人设资源和领域上下文",
        ],
        "口播稿正文": _build_body(topic, note),
        "稿件结构概览": {
            "hook": "从情绪和冲突切入热点问题",
            "deep_dive": "解释技术或产品本质，并给出类比",
            "impact": "回到行业影响与实际判断",
        },
    }
