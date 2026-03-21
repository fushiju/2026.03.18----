"""登录模块测试 — 10 条用例

用例来源：用户端_登录.xlsx
测试类分组：
  TestLoginSuccess   — 正向登录成功
  TestCaptcha        — 验证码相关（刷新、格式、错误）
  TestEmptyFields    — 空字段前端校验
  TestWrongCredentials — 错误凭据
"""
import pytest
from pages.login_page import LoginPage
from config.settings import ADMIN_USERNAME, ADMIN_PASSWORD


# ---------------------------------------------------------------------------
# 辅助常量
# ---------------------------------------------------------------------------
WRONG_PASSWORD = "wrongpassword999"
NONEXISTENT_USER = "nonexistentuser888"
WRONG_USERNAME = "fushuju"


# ===========================================================================
# 正向：登录成功
# ===========================================================================
@pytest.mark.login
class TestLoginSuccess:

    @pytest.mark.smoke
    def test_01_correct_login(self, login_page: LoginPage):
        """TC-01 正确账号密码登录 — 应跳转到 dashboard，页面显示 admin"""
        success = login_page.login_with_captcha(ADMIN_USERNAME, ADMIN_PASSWORD)

        # 断言1：login_with_captcha 返回 True（内部判断 URL 不含 "login"）
        assert success, "login_with_captcha 返回 False，预期登录成功后返回 True"

        # 断言2：当前 URL 不含 "login" 且含 "dashboard"（至少满足其一）
        current_url = login_page.current_url
        assert "login" not in current_url or "dashboard" in current_url, (
            f"登录后 URL 不符合预期，实际 URL: {current_url}"
        )

        # 断言3：页面内容包含用户名 "admin"（顶栏/用户头像/欢迎语等）
        page_content = login_page.page.content()
        assert ADMIN_USERNAME in page_content, (
            f"登录后页面未显示用户名 '{ADMIN_USERNAME}'"
        )


# ===========================================================================
# 验证码相关
# ===========================================================================
@pytest.mark.login
class TestCaptcha:

    def test_02_captcha_refresh(self, login_page: LoginPage):
        """TC-02 验证码刷新功能 — 点击 canvas 后截图字节应改变"""
        before = login_page.get_captcha_image_bytes()
        assert before, "点击前验证码 canvas 截图为空，无法进行对比"

        login_page.click_captcha_image()

        after = login_page.get_captcha_image_bytes()
        assert after, "点击后验证码 canvas 截图为空"
        assert before != after, (
            "点击验证码后图片未发生变化，验证码刷新功能可能失效"
        )

    def test_06_captcha_format(self, login_page: LoginPage):
        """TC-06 验证码格式校验 — 输入含大写字母的验证码，应提示格式错误"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password(ADMIN_PASSWORD)
        # 故意填入含大写字母的验证码（系统要求小写字母+数字）
        login_page.fill_captcha("AbC1")
        login_page.click_login()

        error = login_page.get_error_message()
        assert error, "预期出现验证码格式错误提示，但未检测到任何错误消息"
        assert any(kw in error for kw in ("验证码", "格式", "大写", "小写")), (
            f"错误消息未提及验证码格式问题，实际消息: '{error}'"
        )

    def test_08_wrong_captcha(self, login_page: LoginPage):
        """TC-08 错误验证码登录 — 填入故意错误的验证码，应提示验证码错误并刷新"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password(ADMIN_PASSWORD)
        # 截取错误验证码提交前的 canvas（用于验证后续刷新）
        canvas_before = login_page.get_captcha_image_bytes()

        # 填入明显错误的验证码字符串
        login_page.fill_captcha("zzzz")
        login_page.click_login()
        login_page.page.wait_for_timeout(1500)

        # 断言1：出现错误提示，且提示包含"验证码"
        error = login_page.get_error_message()
        assert error, "预期出现验证码错误提示，但未检测到任何错误消息"
        assert "验证码" in error, (
            f"错误消息未提及验证码，实际消息: '{error}'"
        )

        # 断言2：验证码 canvas 应已刷新（图像内容改变）
        canvas_after = login_page.get_captcha_image_bytes()
        if canvas_before and canvas_after:
            assert canvas_before != canvas_after, (
                "验证码输入错误后，canvas 未刷新"
            )


# ===========================================================================
# 空字段前端校验
# ===========================================================================
@pytest.mark.login
class TestEmptyFields:

    def test_03_empty_username(self, login_page: LoginPage):
        """TC-03 空用户名登录 — 用户名为空时应提示用户名不能为空"""
        login_page.fill_username("")
        login_page.fill_password(ADMIN_PASSWORD)
        # 填入任意验证码，避免验证码校验先于用户名校验触发
        login_page.fill_captcha("test")
        login_page.click_login()

        error = login_page.get_error_message()
        assert error, "预期出现用户名校验错误提示，但未检测到任何错误消息"
        assert "用户名" in error, (
            f"错误消息未提及用户名，实际消息: '{error}'"
        )

    def test_04_empty_password(self, login_page: LoginPage):
        """TC-04 空密码登录 — 密码为空时应提示密码不能为空"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password("")
        # 填入任意验证码，避免验证码校验先于密码校验触发
        login_page.fill_captcha("test")
        login_page.click_login()

        error = login_page.get_error_message()
        assert error, "预期出现密码校验错误提示，但未检测到任何错误消息"
        assert "密码" in error, (
            f"错误消息未提及密码，实际消息: '{error}'"
        )

    def test_05_empty_captcha(self, login_page: LoginPage):
        """TC-05 空验证码登录 — 验证码为空时应提示验证码不能为空"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password(ADMIN_PASSWORD)
        login_page.fill_captcha("")
        login_page.click_login()

        error = login_page.get_error_message()
        assert error, "预期出现验证码校验错误提示，但未检测到任何错误消息"
        assert "验证码" in error, (
            f"错误消息未提及验证码，实际消息: '{error}'"
        )


# ===========================================================================
# 错误凭据（服务端校验）
# ===========================================================================
@pytest.mark.login
class TestWrongCredentials:

    def test_07_wrong_password(self, login_page: LoginPage):
        """TC-07 错误密码登录 — 正确用户名 + 错误密码，服务端应拒绝登录"""
        success = login_page.login_with_captcha(ADMIN_USERNAME, WRONG_PASSWORD)

        assert not success, "错误密码登录不应成功"

        error = login_page.get_error_message()
        assert error, "预期出现登录失败错误提示，但未检测到任何错误消息"
        assert any(kw in error for kw in ("用户名", "密码", "错误", "不正确", "失败")), (
            f"错误消息不符合预期，实际消息: '{error}'"
        )

    def test_09_nonexistent_user(self, login_page: LoginPage):
        """TC-09 不存在的用户名登录 — 系统应拒绝，不泄露账号是否存在"""
        success = login_page.login_with_captcha(NONEXISTENT_USER, WRONG_PASSWORD)

        assert not success, "不存在的用户名不应登录成功"

        error = login_page.get_error_message()
        assert error, "预期出现登录失败错误提示，但未检测到任何错误消息"
        assert any(kw in error for kw in ("用户名", "密码", "错误", "不正确", "失败", "不存在")), (
            f"错误消息不符合预期，实际消息: '{error}'"
        )

    def test_10_wrong_username(self, login_page: LoginPage):
        """TC-10 验证用户名错误 — 错误用户名 'fushuju' + 正确密码，应拒绝登录"""
        success = login_page.login_with_captcha(WRONG_USERNAME, ADMIN_PASSWORD)

        assert not success, f"错误用户名 '{WRONG_USERNAME}' 不应登录成功"

        error = login_page.get_error_message()
        assert error, "预期出现登录失败错误提示，但未检测到任何错误消息"
        assert any(kw in error for kw in ("用户名", "错误", "不正确", "失败", "不存在")), (
            f"错误消息不符合预期，实际消息: '{error}'"
        )
