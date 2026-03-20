"""
登录鉴权接口测试

测试范围:
- 后台管理系统登录/登出
- Token验证
- 未登录访问受保护接口
- 权限校验
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import TestConfig
from utils.api_client import APIClient


class TestAdminLogin:
    """后台管理系统登录"""

    @pytest.mark.P0
    @pytest.mark.smoke
    def test_login_success(self):
        """正确账号密码登录成功"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.login(TestConfig.ADMIN_USERNAME, TestConfig.ADMIN_PASSWORD)
        # 根据实际接口调整断言
        assert resp.status_code in (200, 201), f"登录失败: {resp.text}"

    @pytest.mark.P0
    def test_login_wrong_password(self):
        """错误密码登录失败"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.post("/auth/login", json={
            "username": TestConfig.ADMIN_USERNAME,
            "password": "wrong_password_123",
        })
        assert resp.status_code in (401, 403, 400), "错误密码应登录失败"

    @pytest.mark.P0
    def test_login_empty_username(self):
        """空用户名登录失败"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.post("/auth/login", json={
            "username": "",
            "password": TestConfig.ADMIN_PASSWORD,
        })
        assert resp.status_code in (400, 401, 422)

    @pytest.mark.P0
    def test_login_empty_password(self):
        """空密码登录失败"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.post("/auth/login", json={
            "username": TestConfig.ADMIN_USERNAME,
            "password": "",
        })
        assert resp.status_code in (400, 401, 422)

    @pytest.mark.P1
    def test_login_nonexistent_user(self):
        """不存在的用户登录失败"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.post("/auth/login", json={
            "username": "nonexistent_user_xyz",
            "password": "whatever",
        })
        assert resp.status_code in (401, 403, 404)

    @pytest.mark.P1
    def test_login_sql_injection(self):
        """SQL注入尝试"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.post("/auth/login", json={
            "username": "' OR 1=1 --",
            "password": "' OR '1'='1",
        })
        assert resp.status_code in (400, 401, 403), "SQL注入不应登录成功"

    @pytest.mark.P1
    def test_login_xss_in_username(self):
        """XSS注入尝试"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        resp = client.post("/auth/login", json={
            "username": "<script>alert('xss')</script>",
            "password": "test",
        })
        assert resp.status_code in (400, 401)
        # 确保响应中不包含未转义的脚本
        if resp.text:
            assert "<script>" not in resp.text, "响应中包含未转义的XSS脚本"


class TestTokenValidation:
    """Token验证"""

    @pytest.mark.P0
    @pytest.mark.security
    def test_access_without_token(self, anon_client):
        """未登录访问受保护接口返回401"""
        resp = anon_client.get("/api/orders")
        assert resp.status_code in (401, 403), (
            f"未登录应返回401/403，实际返回 {resp.status_code}"
        )

    @pytest.mark.P0
    @pytest.mark.security
    def test_access_with_invalid_token(self):
        """无效token访问受保护接口"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        client.set_token("invalid_token_12345")
        resp = client.get("/api/orders")
        assert resp.status_code in (401, 403)

    @pytest.mark.P0
    @pytest.mark.security
    def test_access_with_expired_token(self):
        """过期token访问受保护接口"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        # 构造一个格式正确但已过期的JWT (示例)
        expired_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxfQ."
            "invalid_signature"
        )
        client.set_token(expired_token)
        resp = client.get("/api/orders")
        assert resp.status_code in (401, 403)

    @pytest.mark.P0
    def test_access_with_valid_token(self, admin_client):
        """有效token访问受保护接口成功"""
        resp = admin_client.get("/api/orders")
        # 应返回200或有数据的响应
        assert resp.status_code == 200, f"已登录应可访问，实际 {resp.status_code}"
