"""品牌分类模块 fixtures

fixture 与测试文件的对应关系：
  category_page  → test_category_add.py（新增分类）
  category_page  → test_category_edit.py（编辑分类）
  category_page  → test_category_delete.py（删除分类）
"""
import pytest
from pages.brand_category_page import BrandCategoryPage

# 列表中已知的分类
EXISTING_CATEGORY = "会员充值"


@pytest.fixture
def category_page(logged_in_page) -> BrandCategoryPage:
    """已登录 → 品牌分类列表页"""
    bp = BrandCategoryPage(logged_in_page)
    bp.goto_category_list()
    return bp
