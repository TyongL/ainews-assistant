from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class FeishuSettings:
    app_id: str
    app_secret: str
    app_token: str
    news_table_id: str
    doc_folder_token: str
    notes_table_id: str | None = None
    scripts_table_id: str | None = None
    reading_sessions_table_id: str | None = None


def load_feishu_settings(env: Mapping[str, str]) -> FeishuSettings:
    required_keys = [
        "FEISHU_APP_ID",
        "FEISHU_APP_SECRET",
        "FEISHU_APP_TOKEN",
        "FEISHU_NEWS_TABLE_ID",
        "FEISHU_DOC_FOLDER_TOKEN",
    ]
    missing = [key for key in required_keys if not env.get(key)]
    if missing:
        missing_list = ", ".join(missing)
        raise ValueError(f"Missing required Feishu environment variables: {missing_list}")

    return FeishuSettings(
        app_id=env["FEISHU_APP_ID"],
        app_secret=env["FEISHU_APP_SECRET"],
        app_token=env["FEISHU_APP_TOKEN"],
        news_table_id=env["FEISHU_NEWS_TABLE_ID"],
        doc_folder_token=env["FEISHU_DOC_FOLDER_TOKEN"],
        notes_table_id=env.get("FEISHU_NOTES_TABLE_ID"),
        scripts_table_id=env.get("FEISHU_SCRIPTS_TABLE_ID"),
        reading_sessions_table_id=env.get("FEISHU_READING_SESSIONS_TABLE_ID"),
    )


def build_tenant_access_token_request(settings: FeishuSettings) -> dict:
    return {
        "method": "POST",
        "url": "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        "json": {
            "app_id": settings.app_id,
            "app_secret": settings.app_secret,
        },
    }


def build_bitable_record_request(settings: FeishuSettings, fields: Mapping[str, object]) -> dict:
    return {
        "method": "POST",
        "url": (
            "https://open.feishu.cn/open-apis/bitable/v1/apps/"
            f"{settings.app_token}/tables/{settings.news_table_id}/records"
        ),
        "json": {
            "fields": dict(fields),
        },
    }


def build_doc_create_request(settings: FeishuSettings, title: str) -> dict:
    return {
        "method": "POST",
        "url": "https://open.feishu.cn/open-apis/docx/v1/documents",
        "json": {
            "folder_token": settings.doc_folder_token,
            "title": title,
        },
    }


def redact_secret(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def settings_summary(settings: FeishuSettings) -> dict:
    return {
        "app_id": settings.app_id,
        "app_secret": redact_secret(settings.app_secret),
        "app_token": redact_secret(settings.app_token),
        "news_table_id": settings.news_table_id,
        "doc_folder_token": settings.doc_folder_token,
        "notes_table_id": settings.notes_table_id,
        "scripts_table_id": settings.scripts_table_id,
        "reading_sessions_table_id": settings.reading_sessions_table_id,
    }
