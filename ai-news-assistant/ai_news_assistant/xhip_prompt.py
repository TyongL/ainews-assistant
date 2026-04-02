from __future__ import annotations

import json
import os
import re
from pathlib import Path

import requests


DEFAULT_API_KEY_ENV = "BIJI_API_KEY"
DEFAULT_CLIENT_ID_ENV = "BIJI_CLIENT_ID"
DEFAULT_LOCAL_KB_DIR = Path(r"D:\工作\AIProject\项目\IP智能体\get笔记导出")
DEFAULT_KB_ID = "0"
DEFAULT_API_URL = "https://openapi.biji.com/open/api/v1/resource/recall"


def _strip_html_to_text(html: str) -> str:
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</p\s*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</div\s*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<[^>]+>", "", html)
    text = html.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def _tokenize_query(query: str) -> list[str]:
    tokens = re.split(r"[\s,，。;；:：!?！？/\\\-_\(\)\[\]\{\}]+", (query or "").strip())
    tokens = [t for t in tokens if t]
    if not tokens:
        return []
    keep: list[str] = []
    for token in tokens:
        if len(token) >= 2:
            keep.append(token)
        elif re.search(r"[A-Za-z0-9]", token):
            keep.append(token)
    return keep


def search_local_kb(query: str, kb_dir: Path, *, max_files: int = 4000, top_k: int = 5) -> str:
    kb_dir = Path(kb_dir)
    if not kb_dir.exists() or not kb_dir.is_dir():
        return f"[本地知识库] 未找到目录：{kb_dir}"

    tokens = _tokenize_query(query)
    if not tokens:
        return "[本地知识库] 查询为空，跳过。"

    candidates: list[Path] = []
    for pattern in ("*.html", "*.htm", "*.md", "*.txt"):
        candidates.extend(kb_dir.rglob(pattern))
        if len(candidates) >= max_files:
            break

    scored: list[tuple[int, Path, str]] = []
    for path in candidates[:max_files]:
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        text = _strip_html_to_text(raw) if path.suffix.lower() in (".html", ".htm") else raw
        if not text:
            continue

        score = 0
        for token in tokens:
            if token in text:
                score += 3
            elif token.lower() in text.lower():
                score += 1

        if score <= 0:
            continue

        lower_text = text.lower()
        hit_idx = 0
        for token in tokens:
            idx = lower_text.find(token.lower())
            if idx != -1:
                hit_idx = idx
                break
        start = max(0, hit_idx - 220)
        end = min(len(text), hit_idx + 820)
        snippet = text[start:end].strip()
        scored.append((score, path, snippet))

    if not scored:
        return "[本地知识库] 未检索到相关内容。"

    scored.sort(key=lambda item: item[0], reverse=True)
    blocks = ["[本地知识库] 检索结果（按相关度排序）："]
    for score, path, snippet in scored[:top_k]:
        rel = str(path.relative_to(kb_dir)) if str(path).startswith(str(kb_dir)) else str(path)
        blocks.append(f"\n- 文件: {rel}\n  相关度: {score}\n  摘要: {snippet[:1200]}")
    return "\n".join(blocks)


def search_knowledge_base_remote(
    query: str,
    *,
    api_key: str,
    client_id: str,
    api_url: str,
    kb_id: str,
    timeout_sec: int = 30,
) -> str:
    if not api_key or not client_id:
        return "[错误] 未提供 BIJI API Key 或 Client ID。"

    headers = {
        "Authorization": api_key,
        "X-Client-ID": client_id,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    payload: dict[str, object] = {
        "query": query,
        "top_k": 5,
    }
    if kb_id and kb_id.isdigit():
        payload["knowledge_id"] = int(kb_id)

    try:
        session = requests.Session()
        session.trust_env = False
        response = session.post(api_url, json=payload, headers=headers, timeout=(10, max(timeout_sec, 120)))
        if response.status_code != 200:
            return f"[错误] API 请求失败 (状态码: {response.status_code})。"
        data = response.json()
        if "data" in data and isinstance(data["data"], list):
            results = data["data"]
            if not results:
                return "[远程知识库] 未检索到相关内容。"
            blocks = ["[远程知识库] 检索结果："]
            for item in results:
                title = item.get("title", "未命名笔记")
                content = item.get("content", "")
                if isinstance(content, list):
                    content = "\n".join(content)
                blocks.append(f"\n- 笔记: {title}\n  内容: {str(content)[:1500]}")
            return "\n".join(blocks)
        if "c" in data and "answers" in data["c"]:
            return data["c"]["answers"]
        return f"[信息] 检索成功但数据结构未知: {json.dumps(data, ensure_ascii=False)[:1000]}"
    except Exception as exc:
        return f"[错误] 连接到知识库失败: {exc}"


def load_xhip_resources(skill_root: Path) -> tuple[str, str]:
    docs_dir = skill_root / "docs" / "xhip"
    logic = (docs_dir / "logic_and_style.md").read_text(encoding="utf-8")
    tone = (docs_dir / "tone_and_persona.md").read_text(encoding="utf-8")
    return logic, tone


def generate_xhip_prompt(topic: str, kb_context: str, logic: str, tone: str, user_content: str = "") -> str:
    return f"""
# 角色: 晓辉博士 (Dr. Xiaohui)

## 核心人设
{tone}

## 思维逻辑与结构
{logic}

## 当前任务
为主题生成短视频脚本 (口播稿): "{topic}"

### 来自知识库的上下文
[知识库上下文开始]
{kb_context}
[知识库上下文结束]

### 来自用户的上下文
[用户上下文开始]
{user_content}
[用户上下文结束]

## 输出要求
1. 最终输出必须仅为脚本
2. 以 Hook 开始
3. 以 "拜拜" 结束
4. 在正文前必须单独一行输出标题
5. 格式：`Title: [标题内容]`
"""


def write_xhip_prompt_file(skill_root: Path, prompt: str) -> Path:
    outputs_dir = skill_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = outputs_dir / "temp_prompt_for_agent.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    return prompt_path


def load_url_or_content(url: str | None = None, content: str | None = None, content_file: str | None = None) -> str:
    if content:
        return content
    if content_file:
        return Path(content_file).read_text(encoding="utf-8", errors="ignore")
    if not url:
        return ""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text[:5000]
        return ""
    except Exception:
        return ""


def build_kb_context(topic: str, *, kb_mode: str, api_key: str, client_id: str, api_url: str, kb_id: str, kb_dir: Path, timeout_sec: int) -> str:
    kb_context = ""
    if kb_mode != "off":
        if kb_mode in ("auto", "remote"):
            kb_context = search_knowledge_base_remote(
                topic,
                api_key=api_key,
                client_id=client_id,
                api_url=api_url,
                kb_id=kb_id,
                timeout_sec=timeout_sec,
            )
        if kb_mode in ("auto", "local") and (
            (not kb_context)
            or str(kb_context).startswith("[错误]")
            or "连接到知识库失败" in str(kb_context)
        ):
            kb_context = search_local_kb(topic, kb_dir)
    else:
        kb_context = "[知识库已关闭]"
    return kb_context
