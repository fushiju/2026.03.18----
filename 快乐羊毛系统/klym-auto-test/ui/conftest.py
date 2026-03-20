"""
UI 测试 conftest - 提供 Playwright 浏览器和已登录页面
"""
import pytest
from playwright.sync_api import sync_playwright, Page

from common.config import Config
from common.logger import logger
from ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context():
    """创建浏览器上下文（整个测试会话共享）"""
    with sync_playwright() as p:
        browser_type = getattr(p, Config.BROWSER_TYPE)
        browser = browser_type.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context) -> Page:
    """创建新页面（每个测试用例一个）"""
    page = browser_context.new_page()
    page.set_default_timeout(Config.ELEMENT_TIMEOUT)
    yield page
    page.close()


@pytest.fixture
def admin_page(browser_context) -> Page:
    """创建已登录管理员的页面"""
    page = browser_context.new_page()
    page.set_default_timeout(Config.ELEMENT_TIMEOUT)
    login_page = LoginPage(page)
    login_page.login_as_admin()
    yield page
    page.close()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """测试失败时自动截图"""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        test_name = request.node.name.replace("/", "_").replace("::", "_")
        page.screenshot(
            path=f"{Config.SCREENSHOTS_DIR}/FAIL_{test_name}.png"
        )
        logger.error(f"测试失败截图: FAIL_{test_name}.png")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """将测试结果附加到 request.node 上，供 screenshot_on_failure 使用"""
    import pytest
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
