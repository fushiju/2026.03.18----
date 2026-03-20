"""
pytest全局配置和fixtures

提供所有测试共用的fixtures:
- API客户端（已登录/未登录）
- 测试数据清理
- 临时文件管理
"""
import pytest
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(__file__))

from config import TestConfig
from utils.api_client import APIClient


# ============================================================
# API客户端 Fixtures
# ============================================================

@pytest.fixture(scope="session")
def admin_client():
    """
    已登录的后台管理员API客户端（session级别，整个测试会话共用）

    使用方法:
        def test_xxx(self, admin_client):
            resp = admin_client.get("/api/orders")
    """
    client = APIClient(TestConfig.ADMIN_BASE_URL)
    client.login(TestConfig.ADMIN_USERNAME, TestConfig.ADMIN_PASSWORD)
    yield client


@pytest.fixture
def anon_client():
    """
    未登录的API客户端（每个测试函数独立）

    用于测试:
    - 未登录访问受保护接口 -> 401
    - 登录接口本身
    """
    client = APIClient(TestConfig.ADMIN_BASE_URL)
    yield client


@pytest.fixture
def brand_client():
    """品牌主账号API客户端"""
    client = APIClient(TestConfig.ADMIN_BASE_URL)
    brand = TestConfig.TEST_MERCHANT_BRAND
    client.login(brand.get("username", "test_brand"), "test123")
    yield client


@pytest.fixture
def store_client():
    """门店子账号API客户端"""
    client = APIClient(TestConfig.ADMIN_BASE_URL)
    store = TestConfig.TEST_MERCHANT_STORES[0]
    client.login(store.get("username", "test_store1"), "test123")
    yield client


# ============================================================
# 临时文件 Fixtures
# ============================================================

@pytest.fixture
def temp_dir():
    """临时目录（测试结束自动清理）"""
    d = tempfile.mkdtemp(prefix="klym_test_")
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def temp_excel(temp_dir):
    """临时Excel文件路径"""
    return os.path.join(temp_dir, "test_import.xlsx")


@pytest.fixture
def temp_image(temp_dir):
    """临时图片文件路径"""
    return os.path.join(temp_dir, "test_image.jpg")


# ============================================================
# Playwright Fixtures（UI测试用）
# ============================================================

@pytest.fixture(scope="session")
def browser_context_args():
    """Playwright浏览器配置"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai",
    }


# ============================================================
# 测试报告增强
# ============================================================

def pytest_html_report_title(report):
    """自定义HTML报告标题"""
    report.title = "快乐羊毛平台 - 自动化测试报告"
