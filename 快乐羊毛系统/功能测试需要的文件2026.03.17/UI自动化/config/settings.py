"""项目全局配置 - 优先从环境变量读取，回退到默认值"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = os.getenv("KLYM_BASE_URL", "https://red.jinyedaojia.com/")
ADMIN_USERNAME = os.getenv("KLYM_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("KLYM_PASSWORD", "admin123")
CAPTCHA_BYPASS = os.getenv("KLYM_CAPTCHA_BYPASS", "")
TIMEOUT = 30000
HEADLESS = os.getenv("KLYM_HEADLESS", "false").lower() == "true"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
REPORT_DIR = BASE_DIR / "reports"
TESTCASE_DIR = BASE_DIR.parent / "UI自动化docs" / "测试用例"
