"""
全局 fixtures - 登录、客户端初始化、订单完整流程
"""
import logging
import datetime
import os

import allure
import jsonpath
import pytest

from config import config
from utils.api_client import ApiClient
from utils.db_helper import DBHelper
from utils.commission_calculator import CommissionCalculator
from api.wechat_api import WechatOrderAPI, TechnicianAPI, AdminAPI

logger = logging.getLogger(__name__)

# ---- 日志配置 ----
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def pytest_configure(cfg):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cfg.option.log_file = os.path.join(LOG_DIR, f"pytest_{now}.log")
    cfg.option.log_file_mode = "a"


# ---- Hook: 记录用例结果 ----
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    out = yield
    res = out.get_result()
    if res.when == "call":
        logging.info(f"用例ID: {res.nodeid}")
        logging.info(f"测试结果: {res.outcome}")
        if res.longrepr:
            logging.info(f"失败信息: {res.longrepr}")
        logging.info(f"耗时: {call.duration:.2f}s")
        logging.info("=" * 60)


# ---- Fixtures ----

@pytest.fixture(scope="session")
def api_client():
    """全局 API 客户端"""
    return ApiClient()


@pytest.fixture(scope="session")
def db():
    """数据库查询工具"""
    return DBHelper()


@pytest.fixture(scope="session")
def calculator():
    """分佣计算器"""
    return CommissionCalculator()


@pytest.fixture(scope="session")
def admin_client(api_client):
    """管理后台已登录客户端"""
    client = ApiClient()
    admin_api = AdminAPI(client)
    resp = admin_api.login()
    data = resp.json()
    token = jsonpath.jsonpath(data, "$..token")
    if token:
        client.set_token(token[0])
        logger.info("管理后台登录成功")
    else:
        logger.warning(f"管理后台登录失败: {data}")
    return client


@pytest.fixture(scope="session")
def admin_api(admin_client):
    """管理后台 API"""
    return AdminAPI(admin_client)


@pytest.fixture(scope="session")
def user_client():
    """用户端已登录客户端"""
    client = ApiClient()
    wechat_api = WechatOrderAPI(client)
    phone = config["accounts"]["user"]["phone"]
    resp = wechat_api.user_login(phone)
    data = resp.json()
    token = jsonpath.jsonpath(data, "$..token")
    if token:
        client.set_token(token[0])
        logger.info(f"用户 {phone} 登录成功")
    return client


@pytest.fixture(scope="session")
def tech_client():
    """技师端已登录客户端"""
    client = ApiClient()
    tech_api = TechnicianAPI(client)
    phone = config["accounts"]["technician"]["phone"]
    resp = tech_api.login(phone)
    data = resp.json()
    token = jsonpath.jsonpath(data, "$..token")
    if token:
        client.set_token(token[0])
        logger.info(f"技师 {phone} 登录成功")
    return client


@pytest.fixture(scope="session")
def order_api(user_client):
    """用户端订单 API"""
    return WechatOrderAPI(user_client)


@pytest.fixture(scope="session")
def tech_api(tech_client):
    """技师端 API"""
    return TechnicianAPI(tech_client)


@pytest.fixture
def complete_order_flow(order_api, tech_api):
    """
    完整订单流程工厂 fixture
    返回一个函数，调用后自动完成从下单到服务完成的全流程
    """
    def _create_and_complete(tech_id, service_id, address="测试地址",
                             coupon_id=None, card_id=None,
                             source_type=None, source_id=None):
        with allure.step("创建订单"):
            resp = order_api.create_order(
                tech_id=tech_id,
                service_id=service_id,
                address=address,
                coupon_id=coupon_id,
                card_id=card_id,
                source_type=source_type,
                source_id=source_id,
            )
            order_data = resp.json()
            order_id = jsonpath.jsonpath(order_data, "$..orderId")[0]

        with allure.step("技师接单"):
            tech_api.accept_order(order_id)

        with allure.step("技师确认出发"):
            tech_api.confirm_departure(order_id)

        with allure.step("技师拍照到达"):
            tech_api.confirm_arrival(order_id)

        with allure.step("技师开始服务"):
            tech_api.start_service(order_id)

        with allure.step("技师完成服务"):
            tech_api.complete_service(order_id)

        return order_id

    return _create_and_complete
