"""
快乐羊毛 API 客户端封装
- 自动登录维护 token
- 统一请求日志
- 支持多角色
"""
import requests
from common.config import Config
from common.logger import logger


class KLYMClient:
    """快乐羊毛后台 API 客户端"""

    def __init__(self, base_url=None, username=None, password=None):
        self.base_url = (base_url or Config.BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "KLYM-AutoTest/1.0",
            "Accept": "application/json",
        })
        self.token = None
        if username and password:
            self.login(username, password)

    def login(self, username: str, password: str):
        """登录并获取 token/cookie

        注意：具体的登录接口路径和参数需要根据抓包结果调整
        """
        logger.info(f"登录: {username} @ {self.base_url}")
        resp = self.request(
            "POST",
            "/api/login",
            json={"username": username, "password": password},
            skip_auth=True,
        )
        # 根据实际接口响应结构调整 token 提取逻辑
        data = resp.json()
        if "token" in data:
            self.token = data["token"]
            self.session.headers["Authorization"] = f"Bearer {self.token}"
            logger.info("登录成功，token 已设置")
        elif "data" in data and isinstance(data["data"], dict):
            token = data["data"].get("token") or data["data"].get("access_token")
            if token:
                self.token = token
                self.session.headers["Authorization"] = f"Bearer {self.token}"
                logger.info("登录成功，token 已设置")
        else:
            # 可能使用 cookie 鉴权，session 会自动维护
            logger.info("登录完成（cookie 鉴权模式）")
        return resp

    def request(self, method: str, path: str, skip_auth=False, **kwargs):
        """统一请求方法

        Args:
            method: HTTP 方法 (GET/POST/PUT/DELETE)
            path: 接口路径 (如 /api/orders)
            skip_auth: 是否跳过鉴权检查
            **kwargs: 传递给 requests 的其他参数
        """
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", Config.REQUEST_TIMEOUT)

        logger.debug(f"请求: {method} {url}")
        if "json" in kwargs:
            logger.debug(f"请求体: {kwargs['json']}")

        resp = self.session.request(method, url, **kwargs)

        logger.debug(f"响应: {resp.status_code} | {resp.text[:500]}")

        if not skip_auth and resp.status_code == 401:
            logger.error("鉴权失败(401)，请检查 token 是否过期")

        return resp

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)


def create_admin_client():
    """创建管理员客户端"""
    return KLYMClient(
        base_url=Config.BASE_URL,
        username=Config.ADMIN_USER,
        password=Config.ADMIN_PASS,
    )


def create_merchant_client():
    """创建商家品牌主账号客户端"""
    return KLYMClient(
        base_url=Config.BASE_URL,
        username=Config.MERCHANT_USER,
        password=Config.MERCHANT_PASS,
    )


def create_store_client():
    """创建门店子账号客户端"""
    return KLYMClient(
        base_url=Config.BASE_URL,
        username=Config.STORE_USER,
        password=Config.STORE_PASS,
    )
