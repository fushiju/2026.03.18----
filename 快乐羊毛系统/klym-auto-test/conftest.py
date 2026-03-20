"""
全局 conftest - 共享 fixtures
"""
import os
import sys
import json
import pytest

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.config import Config


def load_data(filename: str) -> list:
    """加载测试数据 JSON 文件"""
    filepath = os.path.join(Config.TEST_DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session", autouse=True)
def setup_dirs():
    """确保输出目录存在"""
    os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
