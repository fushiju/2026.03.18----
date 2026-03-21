"""登录页 Page Object"""
import time
from pages.base_page import BasePage
from utils.captcha_solver import solve_captcha


class LoginPage(BasePage):
    # --- 实际 DOM 选择器（2026-03-21 通过 Playwright 检查确认） ---
    # 用户名：<input name="username" placeholder="用户名">
    SEL_USERNAME = 'input[name="username"]'
    # 密码：<input name="password" type="password" placeholder="密码">
    SEL_PASSWORD = 'input[name="password"]'
    # 验证码输入框：排除 username 和 password 之后的那个 input
    SEL_CAPTCHA_INPUT = 'input:not([name="username"]):not([name="password"]):not([type="password"])'
    # 验证码图片：canvas 元素（非 img），id="s-canvas"，父容器 .s-canvas
    SEL_CAPTCHA_CANVAS = 'canvas#s-canvas'
    SEL_CAPTCHA_CONTAINER = '.s-canvas'
    # 登录按钮：Element UI primary button
    SEL_LOGIN_BTN = 'button.el-button--primary'
    # 错误提示：Element UI 消息组件
    SEL_ERROR_MSG = '.el-message, .el-form-item__error, .el-notification'

    def goto_login(self):
        self.goto("#/login")
        self.page.wait_for_load_state("networkidle")

    def fill_username(self, value: str):
        self.fill(self.SEL_USERNAME, value)

    def fill_password(self, value: str):
        self.fill(self.SEL_PASSWORD, value)

    def fill_captcha(self, value: str):
        """填写验证码 — 尝试多种选择器定位验证码输入框"""
        selectors = [
            self.SEL_CAPTCHA_INPUT,
            'input[placeholder*="\u9a8c\u8bc1\u7801"]',  # Unicode 编码的 "验证码"
            '.login-code input',
            'input:nth-of-type(3)',
        ]
        for sel in selectors:
            try:
                el = self.page.query_selector(sel)
                if el and el.is_visible():
                    self.page.fill(sel, value)
                    return
            except Exception:
                continue
        # 最后降级：直接用第一个选择器（会报错但给出明确信息）
        self.fill(selectors[0], value)

    def click_login(self):
        self.click(self.SEL_LOGIN_BTN)

    def get_captcha_image_bytes(self) -> bytes:
        """截取验证码 canvas 元素为图片字节"""
        canvas = self.page.query_selector(self.SEL_CAPTCHA_CANVAS)
        if canvas:
            return canvas.screenshot()
        # 降级：截取容器
        container = self.page.query_selector(self.SEL_CAPTCHA_CONTAINER)
        if container:
            return container.screenshot()
        return b""

    def click_captcha_image(self):
        """点击验证码 canvas 刷新验证码"""
        self.click(self.SEL_CAPTCHA_CANVAS)
        time.sleep(0.5)

    def get_error_message(self, timeout: int = 3000) -> str:
        try:
            self.page.wait_for_selector(self.SEL_ERROR_MSG, timeout=timeout)
            elements = self.page.query_selector_all(self.SEL_ERROR_MSG)
            texts = [el.text_content() or "" for el in elements]
            return " ".join(texts).strip()
        except Exception:
            return ""

    def login_with_captcha(self, username: str, password: str, max_retries: int = 3) -> bool:
        """完整登录流程：填写用户名/密码 → OCR 识别验证码 → 点击登录，支持验证码重试"""
        self.fill_username(username)
        self.fill_password(password)
        for attempt in range(max_retries):
            img_bytes = self.get_captcha_image_bytes()
            captcha_text = solve_captcha(img_bytes)
            self.fill_captcha(captcha_text)
            self.click_login()
            self.page.wait_for_timeout(1500)
            # 判断是否登录成功（跳转离开 login 页）
            if "login" not in self.current_url:
                return True
            error = self.get_error_message()
            if "验证码" in error:
                self.click_captcha_image()
                continue
            elif error:
                # 非验证码错误（如密码错误），不再重试
                return False
        return False
