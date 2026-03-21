"""pytest fixtures - 浏览器管理、页面上下文、失败截图"""
import pytest
from playwright.sync_api import sync_playwright
from config.settings import HEADLESS, SCREENSHOT_DIR
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
