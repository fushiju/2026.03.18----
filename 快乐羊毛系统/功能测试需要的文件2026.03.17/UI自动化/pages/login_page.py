"""登录页 Page Object"""
import time
from pages.base_page import BasePage
from utils.captcha_solver import solve_captcha


class LoginPage(BasePage):
    # --- 实际 DOM 选择器（2026-03-21 通过 Playwright 检查确认） ---
    SEL_USERNAME = 'input.el-input__inner[name="username"]'
    SEL_PASSWORD = 'input.el-input__inner[name="password"]'
    SEL_CAPTCHA_INPUT = 'input.el-input__inner[placeholder="\u9a8c\u8bc1\u7801"]'
    SEL_CAPTCHA_CANVAS = 'canvas#s-canvas'
    SEL_CAPTCHA_CONTAINER = '.s-canvas'
    SEL_LOGIN_BTN = 'button.el-button--primary'
    SEL_ERROR_MSG = '.el-message, .el-form-item__error, .el-notification'

    def goto_login(self):
        self.goto("#/login")
        self.page.wait_for_load_state("networkidle")
        # 等待登录表单加载完成
        self.page.wait_for_selector(self.SEL_USERNAME, timeout=10000)

    def fill_username(self, value: str):
        self.page.locator(self.SEL_USERNAME).fill(value)

    def fill_password(self, value: str):
        self.page.locator(self.SEL_PASSWORD).fill(value)

    def fill_captcha(self, value: str):
        self.page.locator(self.SEL_CAPTCHA_INPUT).fill(value)

    def click_login(self):
        self.page.locator(self.SEL_LOGIN_BTN).click()

    def get_captcha_image_bytes(self) -> bytes:
        """截取验证码 canvas 元素为图片字节"""
        canvas = self.page.locator(self.SEL_CAPTCHA_CANVAS)
        if canvas.count() > 0:
            return canvas.screenshot()
        container = self.page.locator(self.SEL_CAPTCHA_CONTAINER)
        if container.count() > 0:
            return container.screenshot()
        return b""

    def click_captcha_image(self):
        """点击验证码 canvas 刷新验证码"""
        self.page.locator(self.SEL_CAPTCHA_CANVAS).click()
        time.sleep(0.5)

    def get_error_message(self, timeout: int = 3000) -> str:
        try:
            self.page.wait_for_selector(self.SEL_ERROR_MSG, timeout=timeout)
            elements = self.page.locator(self.SEL_ERROR_MSG).all()
            texts = [el.text_content() or "" for el in elements]
            return " ".join(texts).strip()
        except Exception:
            return ""

    def login_with_captcha(self, username: str, password: str, max_retries: int = 3) -> bool:
        """完整登录流程：填写用户名/密码 + OCR 识别验证码 + 点击登录，支持验证码重试"""
        self.fill_username(username)
        self.fill_password(password)
        for attempt in range(max_retries):
            img_bytes = self.get_captcha_image_bytes()
            captcha_text = solve_captcha(img_bytes)
            self.fill_captcha(captcha_text)
            self.click_login()
            self.page.wait_for_timeout(2000)
            # 判断是否登录成功
            if "login" not in self.current_url:
                return True
            error = self.get_error_message()
            if "验证码" in error:
                self.click_captcha_image()
                continue
            elif error:
                return False
        return False
