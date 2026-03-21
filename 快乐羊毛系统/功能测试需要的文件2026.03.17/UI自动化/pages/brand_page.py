"""品牌管理页 Page Object"""
from pages.base_page import BasePage


class BrandPage(BasePage):
    # --- DOM 选择器（待实际页面确认后补充） ---

    def goto_brand_list(self):
        """导航到品牌管理列表页"""
        pass

    def add_brand(self, brand_name: str, **kwargs):
        """新增品牌"""
        pass

    def edit_brand(self, brand_name: str, **kwargs):
        """编辑品牌"""
        pass

    def delete_brand(self, brand_name: str):
        """删除品牌"""
        pass

    def search_brand(self, keyword: str):
        """搜索品牌"""
        pass

    def get_brand_list(self) -> list[str]:
        """获取当前页品牌列表"""
        pass
