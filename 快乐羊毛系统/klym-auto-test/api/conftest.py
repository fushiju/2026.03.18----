"""
API 测试 conftest - 提供各角色的 API 客户端
"""
import pytest
from api.client import KLYMClient, create_admin_client
from common.config import Config


@pytest.fixture(scope="session")
def admin_client() -> KLYMClient:
    """后台管理员 API 客户端"""
    return create_admin_client()


@pytest.fixture(scope="session")
def merchant_client() -> KLYMClient:
    """商家品牌主账号 API 客户端（待配置账号后启用）"""
    if not Config.MERCHANT_USER:
        pytest.skip("商家账号未配置")
    return KLYMClient(
        base_url=Config.BASE_URL,
        username=Config.MERCHANT_USER,
        password=Config.MERCHANT_PASS,
    )


@pytest.fixture(scope="session")
def store_client() -> KLYMClient:
    """门店子账号 API 客户端（待配置账号后启用）"""
    if not Config.STORE_USER:
        pytest.skip("门店账号未配置")
    return KLYMClient(
        base_url=Config.BASE_URL,
        username=Config.STORE_USER,
        password=Config.STORE_PASS,
    )


@pytest.fixture
def guest_client() -> KLYMClient:
    """未登录的 API 客户端（用于鉴权测试）"""
    return KLYMClient(base_url=Config.BASE_URL)
