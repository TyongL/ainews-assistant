"""
AI News Assistant - Feishu Integration Layer

使用 OpenClaw 飞书工具封装，而非直接调用 HTTP API
"""
import json
from datetime import datetime
from typing import Any

# 飞书资源配置（从配置读取）
APP_TOKEN = "UzlwbVcTOarp03sOfnZcGX6GnAc"
NEWS_TABLE_ID = "tbl48sDs3PhvXgAi"


def parse_news_items(raw_input: str) -> list[dict]:
    """
    将用户输入的混合资讯拆分成独立的新闻条目
    
    Args:
        raw_input: 用户输入的原始资讯内容
        
    Returns:
        新闻条目列表，每条包含 title, content, source_url, tags
    """
    items = []
    lines = raw_input.strip().split("\n")
    
    current_item = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测新条目（以数字开头或是特殊标记）
        if line[0].isdigit() and (". " in line or "、 " in line):
            # 保存上一条
            if current_item:
                current_item["content"] = "\n".join(current_content)
                items.append(current_item)
            
            # 提取标题
            title = line.split(". ", 1)[1] if ". " in line else line.split("、 ", 1)[1]
            current_item = {
                "title": title,
                "content": "",
                "source_url": "",
                "tags": ["AI新闻"]
            }
            current_content = []
        else:
            if current_item is None:
                # 第一条没有序号，当作整体处理
                current_item = {
                    "title": line[:50] if len(line) > 50 else line,
                    "content": "",
                    "source_url": "",
                    "tags": ["AI新闻"]
                }
            current_content.append(line)
    
    # 保存最后一条
    if current_item:
        current_item["content"] = "\n".join(current_content)
        items.append(current_item)
    
    return items


def create_news_record(title: str, content: str, source_url: str = "", tags: list = None, status: str = "ingested") -> dict:
    """
    在飞书 Bitable 中创建一条资讯记录
    
    Returns:
        创建的记录对象
    """
    from feishu_bitable_create_record import create_record
    
    fields = {
        "标题": title,
        "原始内容": content,
        "日期": int(datetime.now().timestamp() * 1000),
        "状态": status
    }
    
    if source_url:
        fields["来源链接"] = {"text": source_url, "link": source_url}
    
    if tags:
        fields["标签"] = tags
    
    # 这里使用模拟返回值，实际会通过工具调用
    return {
        "app_token": APP_TOKEN,
        "table_id": NEWS_TABLE_ID,
        "fields": fields
    }


def list_news_records(limit: int = 20, status: str = None) -> dict:
    """
    获取资讯列表
    
    Args:
        limit: 返回数量限制
        status: 按状态过滤
    """
    return {
        "app_token": APP_TOKEN,
        "table_id": NEWS_TABLE_ID,
        "page_size": limit
    }


def create_daily_report(news_items: list, date: str = None) -> dict:
    """
    创建每日简报文档
    
    Args:
        news_items: 资讯列表
        date: 日期，默认为今天
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    content_lines = [
        f"# AI资讯日报 {date}",
        "",
        "## 今日资讯",
        ""
    ]
    
    for i, item in enumerate(news_items, 1):
        content_lines.append(f"### {i}. {item.get('title', '无标题')}")
        content_lines.append("")
        content_lines.append(f"- **来源**: {item.get('source_url', '未知')}")
        content_lines.append(f"- **标签**: {', '.join(item.get('tags', []))}")
        content_lines.append(f"- **状态**: {item.get('status', 'ingested')}")
        content_lines.append("")
        if item.get('content'):
            content_lines.append(f"**摘要**: {item['content'][:200]}...")
        content_lines.append("")
    
    content_lines.append("---")
    content_lines.append("*由 AI资讯助手 自动生成*")
    
    return {
        "title": f"AI资讯日报_{date}",
        "content": "\n".join(content_lines)
    }


def update_news_status(record_id: str, new_status: str) -> dict:
    """
    更新资讯状态
    
    Args:
        record_id: 记录 ID
        new_status: 新状态
    """
    return {
        "app_token": APP_TOKEN,
        "table_id": NEWS_TABLE_ID,
        "record_id": record_id,
        "fields": {"状态": new_status}
    }


def create_note_document(title: str, news_content: str, discussion_points: list) -> dict:
    """
    创建笔记文档
    
    Args:
        title: 笔记标题
        news_content: 原始资讯内容
        discussion_points: 讨论要点
    """
    content_lines = [
        f"# {title}",
        "",
        "## 原始内容",
        "",
        news_content,
        "",
        "## 讨论要点",
        ""
    ]
    
    for i, point in enumerate(discussion_points, 1):
        content_lines.append(f"{i}. {point}")
    
    content_lines.append("")
    content_lines.append("---")
    content_lines.append("*由 AI资讯助手 整理*")
    
    return {
        "title": f"AI资讯笔记_{title}",
        "content": "\n".join(content_lines)
    }


def generate_script(note_content: str, style: str = "短视频口播") -> str:
    """
    根据笔记生成口播稿
    
    Args:
        note_content: 笔记内容
        style: 口播风格
    """
    # 这是一个占位符，实际由 LLM 生成
    return f"""# {style}口播稿

（开头）
大家好，今天来聊聊一条有趣的AI资讯...

（正文）
{note_content[:500]}...

（结尾）
好了，这就是今天的分享，记得关注我了解更多AI资讯！

（完）
"""