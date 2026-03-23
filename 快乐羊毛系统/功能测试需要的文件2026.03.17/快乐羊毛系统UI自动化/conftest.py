"""pytest fixtures - 浏览器管理、页面上下文、失败截图"""
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from config.settings import HEADLESS, SCREENSHOT_DIR, REPORT_DIR, ADMIN_USERNAME, ADMIN_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            args=["--ignore-certificate-errors", "--disable-web-security"]
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(ignore_https_errors=True)
    pg = context.new_page()
    yield pg
    pg.close()
    context.close()


@pytest.fixture
def login_page(page) -> LoginPage:
    lp = LoginPage(page)
    lp.goto_login()
    return lp


@pytest.fixture
def logged_in_page(page) -> "Page":
    """登录后的页面，供需要登录态的测试使用"""
    lp = LoginPage(page)
    lp.goto_login()
    success = lp.login_with_captcha(ADMIN_USERNAME, ADMIN_PASSWORD)
    assert success, "前置条件：登录失败，无法继续执行测试"
    # 登录后等待页面稳定，关闭可能弹出的通知弹窗（如"来单通知"）
    page.wait_for_timeout(2000)
    _dismiss_all_dialogs(page)
    return page


def _dismiss_all_dialogs(page):
    """关闭所有可能遮挡页面的弹窗（来单通知、消息框等）"""
    try:
        for _ in range(5):
            btn = page.locator(
                '.el-dialog:visible button:has-text("忽 略"), '
                '.el-dialog:visible button:has-text("忽略"), '
                '.el-dialog:visible button:has-text("关闭"), '
                '.el-dialog:visible .el-dialog__headerbtn, '
                '.el-message-box__btns button:has-text("确定")'
            )
            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(800)
            else:
                break
    except Exception:
        pass


@pytest.fixture(scope="session")
def test_fixtures_dir() -> Path:
    """测试数据文件目录"""
    return Path(__file__).resolve().parent / "tests" / "fixtures"


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        name = request.node.name.replace("[", "_").replace("]", "")
        page.screenshot(path=str(SCREENSHOT_DIR / f"FAIL_{name}.png"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """修复 Windows 中文环境下 HTML 报告乱码：重新以 UTF-8 编码保存"""
    report_file = REPORT_DIR / "login_report.html"
    if report_file.exists():
        raw = report_file.read_bytes()
        # 尝试以 GBK 解码再以 UTF-8 重写；如果本身就是 UTF-8 则跳过
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("gbk", errors="replace")
        # 确保 <head> 中有 charset=utf-8
        if '<meta charset="utf-8">' not in text:
            text = text.replace("<head>", '<head>\n<meta charset="utf-8">', 1)
        report_file.write_bytes(text.encode("utf-8"))
