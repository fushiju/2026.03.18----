"""品牌管理模块 fixtures

为新增/编辑/查看/搜索四个场景提供各自的 fixture，
避免所有测试都先进入新增品牌页面再跳转。
"""
import pytest
from pages.brand_page import BrandPage

# 列表中已知的测试品牌（已授权→可编辑，已驳回→可查看）
EDIT_BRAND_NAME = "小王"
VIEW_BRAND_NAME = "周六"


@pytest.fixture
def brand_page(logged_in_page) -> BrandPage:
    """仅登录，返回 BrandPage 实例（不导航到任何子页面）"""
    return BrandPage(logged_in_page)


@pytest.fixture
def brand_add_page(logged_in_page) -> BrandPage:
    """已登录并进入【新增品牌】页面"""
    bp = BrandPage(logged_in_page)
    bp.goto_add_brand()
    return bp


@pytest.fixture
def brand_edit_page(logged_in_page) -> BrandPage:
    """已登录并进入【编辑品牌】页面（编辑品牌 '小王'）"""
    bp = BrandPage(logged_in_page)
    bp.goto_edit_brand(EDIT_BRAND_NAME)
    return bp


@pytest.fixture
def brand_view_page(logged_in_page) -> BrandPage:
    """已登录并进入【查看品牌】页面（查看品牌 '周六'）"""
    bp = BrandPage(logged_in_page)
    bp.goto_view_brand(VIEW_BRAND_NAME)
    return bp


@pytest.fixture
def brand_list_page(logged_in_page) -> BrandPage:
    """已登录并进入【品牌管理列表】页面"""
    bp = BrandPage(logged_in_page)
    bp.goto_brand_list()
    bp._dismiss_notification()
    return bp
