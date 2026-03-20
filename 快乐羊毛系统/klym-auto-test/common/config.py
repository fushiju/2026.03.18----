"""
环境配置 - 快乐羊毛自动化测试
"""
import os


class Config:
    """测试环境配置"""

    # 快乐羊毛后台
    BASE_URL = os.getenv("KLYM_BASE_URL", "https://red.jinyedaojia.com")
    ADMIN_USER = os.getenv("KLYM_ADMIN_USER", "admin")
    ADMIN_PASS = os.getenv("KLYM_ADMIN_PASS", "admin123")

    # 今夜到家后台（旧系统）
    JYDJ_BASE_URL = os.getenv("JYDJ_BASE_URL", "https://develop1.jinyedaojia.com")
    JYDJ_ADMIN_USER = os.getenv("JYDJ_ADMIN_USER", "admin")
    JYDJ_ADMIN_PASS = os.getenv("JYDJ_ADMIN_PASS", "admin#$%")

    # 商家账号（待配置）
    MERCHANT_USER = os.getenv("KLYM_MERCHANT_USER", "")
    MERCHANT_PASS = os.getenv("KLYM_MERCHANT_PASS", "")

    # 门店子账号（待配置）
    STORE_USER = os.getenv("KLYM_STORE_USER", "")
    STORE_PASS = os.getenv("KLYM_STORE_PASS", "")

    # 超时设置（秒）
    REQUEST_TIMEOUT = 30
    PAGE_LOAD_TIMEOUT = 30000  # Playwright 使用毫秒
    ELEMENT_TIMEOUT = 10000

    # 路径
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
    REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
    TEST_DATA_DIR = os.path.join(PROJECT_ROOT, "common", "data")

    # 浏览器配置
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # 毫秒，调试时可设大一些
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")  # chromium/firefox/webkit
