"""登录页 Page Object"""
import time
from pages.base_page import BasePage
from utils.captcha_solver import solve_captcha


class LoginPage(BasePage):
    # --- 实际 DOM 选择器（2026-03-21 通过 Playwright 检查确认） ---
    SEL_USERNAME = 'input.el-input__inner[name="username"]'
    SEL_PASSWORD = 'input.el-input__inner[name="password"]'
    SEL_CAPTCHA_INPUT = '.el-form-item:nth-child(3) input'
    SEL_CAPTCHA_CANVAS = 'canvas#s-canvas'
    SEL_CAPTCHA_CONTAINER = '.s-canvas'
    SEL_LOGIN_BTN = 'button.el-button--primary'
    SEL_ERROR_MSG = '.el-message, .el-form-item__error, .el-notification'

    def goto_login(self, max_retries: int = 3):
        """打开登录页，网络不稳定时自动重试"""
        from config.settings import BASE_URL
        url = f"{BASE_URL.rstrip('/')}/#/login"
        for attempt in range(max_retries):
            try:
                self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
                self.page.wait_for_selector(self.SEL_USERNAME, state="visible", timeout=15000)
                self.page.wait_for_selector(self.SEL_CAPTCHA_INPUT, state="visible", timeout=15000)
                return  # 成功加载
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  页面加载失败（第{attempt+1}次），2秒后重试: {e}")
                    time.sleep(2)
                else:
                    raise

    def fill_username(self, value: str):
        self.page.locator(self.SEL_USERNAME).fill(value)

    def fill_password(self, value: str):
        self.page.locator(self.SEL_PASSWORD).fill(value)

    def fill_captcha(self, value: str):
        loc = self.page.locator(self.SEL_CAPTCHA_INPUT)
        loc.wait_for(state="visible", timeout=10000)
        loc.fill(value)

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

    def _wait_for_login_result(self, timeout: int = 10) -> str:
        """等待登录结果，返回 'success' / 'captcha_error' / 'other_error' / 'unknown'"""
        for _ in range(timeout * 2):  # 每0.5秒检查一次
            self.page.wait_for_timeout(500)
            # 检查是否跳转离开登录页
            if "login" not in self.current_url:
                return "success"
            # 检查是否有错误提示
            error = self.get_error_message(timeout=500)
            if error:
                if "验证码" in error:
                    return "captcha_error"
                return "other_error"
        return "unknown"

    def login_with_captcha(self, username: str, password: str, max_retries: int = 3) -> bool:
        """完整登录流程：填写用户名/密码 + OCR 识别验证码 + 点击登录，支持验证码重试"""
        self.fill_username(username)
        self.fill_password(password)
        for attempt in range(max_retries):
            # 识别验证码
            img_bytes = self.get_captcha_image_bytes()
            captcha_text = solve_captcha(img_bytes)
            print(f"  [尝试 {attempt+1}/{max_retries}] 验证码识别结果: {captcha_text}")
            self.fill_captcha(captcha_text)
            self.click_login()
            # 等待登录结果（最多10秒）
            result = self._wait_for_login_result(timeout=10)
            print(f"  [尝试 {attempt+1}/{max_retries}] 登录结果: {result}")
            if result == "success":
                return True
            elif result == "captcha_error":
                self.click_captcha_image()
                continue
            elif result == "other_error":
                return False
            else:
                # unknown - 没有跳转也没有错误，可能验证码错了但提示消失了
                self.click_captcha_image()
                continue
        return False
