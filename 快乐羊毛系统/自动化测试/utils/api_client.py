"""
API请求客户端封装

封装HTTP请求，统一处理登录态、请求头、错误处理和日志记录。
"""
import requests
import json
import time
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """快乐羊毛API客户端"""

    def __init__(self, base_url, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.token = None

    def login(self, username, password):
        """
        后台登录，获取token

        :param username: 用户名
        :param password: 密码
        :return: 登录响应
        """
        resp = self.post("/auth/login", json={
            "username": username,
            "password": password,
        })
        if resp.status_code == 200:
            data = resp.json()
            # 根据实际接口返回字段调整
            self.token = data.get("token") or data.get("access_token") or data.get("data", {}).get("token")
            if self.token:
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                logger.info(f"登录成功: {username}")
        return resp

    def set_token(self, token):
        """手动设置token"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        """清除token（模拟未登录状态）"""
        self.token = None
        self.session.headers.pop("Authorization", None)

    def _url(self, path):
        """拼接完整URL"""
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"

    def get(self, path, **kwargs):
        """GET请求"""
        kwargs.setdefault("timeout", self.timeout)
        url = self._url(path)
        logger.debug(f"GET {url}")
        resp = self.session.get(url, **kwargs)
        self._log_response(resp)
        return resp

    def post(self, path, **kwargs):
        """POST请求"""
        kwargs.setdefault("timeout", self.timeout)
        url = self._url(path)
        logger.debug(f"POST {url} body={kwargs.get('json') or kwargs.get('data')}")
        resp = self.session.post(url, **kwargs)
        self._log_response(resp)
        return resp

    def put(self, path, **kwargs):
        """PUT请求"""
        kwargs.setdefault("timeout", self.timeout)
        url = self._url(path)
        logger.debug(f"PUT {url}")
        resp = self.session.put(url, **kwargs)
        self._log_response(resp)
        return resp

    def delete(self, path, **kwargs):
        """DELETE请求"""
        kwargs.setdefault("timeout", self.timeout)
        url = self._url(path)
        logger.debug(f"DELETE {url}")
        resp = self.session.delete(url, **kwargs)
        self._log_response(resp)
        return resp

    def upload(self, path, file_path, field_name="file", **kwargs):
        """文件上传"""
        kwargs.setdefault("timeout", 120)
        url = self._url(path)
        with open(file_path, "rb") as f:
            files = {field_name: f}
            resp = self.session.post(url, files=files, **kwargs)
        self._log_response(resp)
        return resp

    def _log_response(self, resp):
        """记录响应日志"""
        logger.debug(
            f"Response [{resp.status_code}] {resp.url} "
            f"({resp.elapsed.total_seconds():.2f}s)"
        )
        if resp.status_code >= 400:
            logger.warning(f"Error response: {resp.text[:500]}")

    def assert_status(self, resp, expected_status, msg=""):
        """断言HTTP状态码"""
        assert resp.status_code == expected_status, (
            f"{msg} 期望状态码 {expected_status}，实际 {resp.status_code}，"
            f"响应: {resp.text[:300]}"
        )

    def assert_json_field(self, resp, field, expected_value=None):
        """断言JSON响应包含指定字段"""
        data = resp.json()
        assert field in data, f"响应中缺少字段 '{field}'，响应: {data}"
        if expected_value is not None:
            assert data[field] == expected_value, (
                f"字段 '{field}' 期望值 {expected_value}，实际 {data[field]}"
            )


class PerformanceTimer:
    """接口性能计时器"""

    def __init__(self, name=""):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()

    @property
    def elapsed(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0

    def assert_within(self, max_seconds, msg=""):
        """断言响应时间在指定范围内"""
        assert self.elapsed <= max_seconds, (
            f"{msg} 响应时间 {self.elapsed:.2f}秒 超过预期 {max_seconds}秒"
        )
