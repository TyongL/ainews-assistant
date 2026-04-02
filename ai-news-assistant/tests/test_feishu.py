import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ai_news_assistant.feishu import build_bitable_record_request, load_feishu_settings


class LoadFeishuSettingsTests(unittest.TestCase):
    def test_loads_required_environment_values(self) -> None:
        env = {
            "FEISHU_APP_ID": "cli_test_app",
            "FEISHU_APP_SECRET": "secret_test_value",
            "FEISHU_APP_TOKEN": "bascn_test_app_token",
            "FEISHU_NEWS_TABLE_ID": "tbl_news",
            "FEISHU_DOC_FOLDER_TOKEN": "fldcn_folder",
        }

        settings = load_feishu_settings(env)

        self.assertEqual(settings.app_id, "cli_test_app")
        self.assertEqual(settings.app_secret, "secret_test_value")
        self.assertEqual(settings.app_token, "bascn_test_app_token")
        self.assertEqual(settings.news_table_id, "tbl_news")
        self.assertEqual(settings.doc_folder_token, "fldcn_folder")

    def test_raises_when_required_values_are_missing(self) -> None:
        with self.assertRaisesRegex(ValueError, "FEISHU_APP_ID"):
            load_feishu_settings({})


class BuildBitableRecordRequestTests(unittest.TestCase):
    def test_builds_expected_endpoint_and_payload(self) -> None:
        env = {
            "FEISHU_APP_ID": "cli_test_app",
            "FEISHU_APP_SECRET": "secret_test_value",
            "FEISHU_APP_TOKEN": "bascn_test_app_token",
            "FEISHU_NEWS_TABLE_ID": "tbl_news",
            "FEISHU_DOC_FOLDER_TOKEN": "fldcn_folder",
        }
        settings = load_feishu_settings(env)
        fields = {
            "资讯ID": "news-001",
            "标题": "测试资讯",
            "当前状态": "ingested",
        }

        request = build_bitable_record_request(settings, fields)

        self.assertEqual(
            request["url"],
            "https://open.feishu.cn/open-apis/bitable/v1/apps/bascn_test_app_token/tables/tbl_news/records",
        )
        self.assertEqual(request["json"], {"fields": fields})


if __name__ == "__main__":
    unittest.main()
