"""品牌管理模块 fixtures

fixture 与 Page 类的对应关系：
  brand_add_page   → BrandFormPage  → test_brand_add.py
  brand_edit_page  → BrandFormPage  → test_brand_edit.py
  brand_view_page  → BrandViewPage  → test_brand_view.py
  brand_list_page  → BrandListPage  → test_brand_search.py
  brand_form_page  → BrandFormPage  → 编辑测试中需要多步跳转的用例
"""
import pytest
from pages.brand_form_page import BrandFormPage
from pages.brand_list_page import BrandListPage
from pages.brand_view_page import BrandViewPage

# 列表中已知的测试品牌
EDIT_BRAND_NAME = "小王"       # 已授权 → 可编辑
VIEW_BRAND_NAME = "周六"       # 已驳回 → 可查看


# ---------- 新增品牌 ----------
@pytest.fixture
def brand_add_page(logged_in_page) -> BrandFormPage:
    """已登录 → 新增品牌表单页"""
    bp = BrandFormPage(logged_in_page)
    bp.goto_add_brand()
    return bp


# ---------- 编辑品牌 ----------
@pytest.fixture
def brand_edit_page(logged_in_page) -> BrandFormPage:
    """已登录 → 编辑品牌'小王'的表单页"""
    bp = BrandFormPage(logged_in_page)
    bp.goto_edit_brand(EDIT_BRAND_NAME)
    return bp


@pytest.fixture
def brand_form_page(logged_in_page) -> BrandFormPage:
    """已登录，未导航（供需要多步跳转的编辑测试用）"""
    return BrandFormPage(logged_in_page)


# ---------- 查看品牌 ----------
@pytest.fixture
def brand_view_page(logged_in_page) -> BrandViewPage:
    """已登录 → 查看品牌'周六'的详情页"""
    bp = BrandViewPage(logged_in_page)
    bp.goto_view_brand(VIEW_BRAND_NAME)
    return bp


@pytest.fixture
def brand_view_list(logged_in_page) -> BrandViewPage:
    """已登录 → 品牌列表页（供查看测试中从列表操作的用例）"""
    bp = BrandViewPage(logged_in_page)
    bp.goto_brand_list()
    bp._dismiss_notification()
    return bp


# ---------- 品牌搜索 ----------
@pytest.fixture
def brand_list_page(logged_in_page) -> BrandListPage:
    """已登录 → 品牌管理列表页"""
    bp = BrandListPage(logged_in_page)
    bp.goto_brand_list()
    bp._dismiss_notification()
    return bp
