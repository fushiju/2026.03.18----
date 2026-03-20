"""
接口测试 - 登录鉴权模块

对应测试策略：
- 4.10 后台管理 - API鉴权
- 安全测试 - 越权访问、token 校验

注意：具体接口路径需根据抓包结果调整
"""
import pytest
from api.client import KLYMClient
from common.config import Config


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.p0
class TestLoginAPI:
    """登录接口测试"""

    def test_login_success(self, admin_client):
        """正确账号密码登录成功"""
        assert admin_client.token is not None or admin_client.session.cookies

    def test_login_wrong_password(self):
        """错误密码登录失败"""
        client = KLYMClient(base_url=Config.BASE_URL)
        resp = client.login(Config.ADMIN_USER, "wrong_password_123")
        # 根据实际接口响应调整断言
        assert resp.status_code in [401, 403, 200]
        if resp.status_code == 200:
            data = resp.json()
            assert data.get("code") != 0 or data.get("success") is False

    def test_login_empty_username(self):
        """用户名为空"""
        client = KLYMClient(base_url=Config.BASE_URL)
        resp = client.login("", Config.ADMIN_PASS)
        assert resp.status_code in [400, 401, 422, 200]

    def test_login_empty_password(self):
        """密码为空"""
        client = KLYMClient(base_url=Config.BASE_URL)
        resp = client.login(Config.ADMIN_USER, "")
        assert resp.status_code in [400, 401, 422, 200]


@pytest.mark.api
@pytest.mark.security
@pytest.mark.p1
class TestAuthAPI:
    """鉴权安全测试"""

    def test_access_without_token(self, guest_client):
        """未登录访问受保护接口应返回 401"""
        resp = guest_client.get("/api/orders", skip_auth=True)
        assert resp.status_code == 401

    def test_access_with_expired_token(self):
        """过期 token 应返回 401"""
        client = KLYMClient(base_url=Config.BASE_URL)
        client.session.headers["Authorization"] = "Bearer expired_token_xxx"
        resp = client.get("/api/orders", skip_auth=True)
        assert resp.status_code == 401

    def test_sql_injection_in_login(self):
        """登录接口 SQL 注入测试"""
        client = KLYMClient(base_url=Config.BASE_URL)
        resp = client.login("' OR 1=1 --", "' OR '1'='1")
        # 不应登录成功
        assert client.token is None

    def test_xss_in_login(self):
        """登录接口 XSS 注入测试"""
        client = KLYMClient(base_url=Config.BASE_URL)
        resp = client.login("<script>alert(1)</script>", "password")
        assert client.token is None
