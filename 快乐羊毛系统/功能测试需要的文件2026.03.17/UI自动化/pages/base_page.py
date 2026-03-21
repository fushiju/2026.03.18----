"""页面基类 - 封装 Playwright 通用操作"""
from playwright.sync_api import Page
from config.settings import TIMEOUT, SCREENSHOT_DIR


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(TIMEOUT)

    def goto(self, path: str = ""):
        from config.settings import BASE_URL
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)

    def fill(self, selector: str, value: str):
        self.page.fill(selector, value)

    def click(self, selector: str):
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def screenshot(self, name: str):
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        path = SCREENSHOT_DIR / f"{name}.png"
        self.page.screenshot(path=str(path))
        return path

    @property
    def current_url(self) -> str:
        return self.page.url
