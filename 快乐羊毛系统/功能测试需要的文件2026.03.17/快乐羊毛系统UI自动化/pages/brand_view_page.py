"""品牌查看页 Page Object（只读详情）

对应页面：#/coach/manage/edit?isEdit=0&id=xxx
  - test_brand_view.py 使用本类
"""
from pages.base_page import BasePage


class BrandViewPage(BasePage):

    # ================================================================
    # 导航
    # ================================================================

    def goto_brand_list(self):
        from config.settings import BASE_URL
        self.page.goto(f"{BASE_URL.rstrip('/')}/#/coach/manage", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def goto_view_brand(self, brand_name: str):
        self.goto_brand_list()
        self._dismiss_notification()
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("查看")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.page.wait_for_timeout(2000)

    def _dismiss_notification(self):
        try:
            btn = self.page.locator('button:has-text("忽 略"), button:has-text("忽略")')
            if btn.count() > 0:
                btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    # ================================================================
    # 页面判断
    # ================================================================

    def is_on_view_page(self) -> bool:
        return "isEdit=0" in self.current_url

    def is_on_brand_list(self) -> bool:
        return "/coach/manage" in self.current_url and "/edit" not in self.current_url

    def get_view_title(self) -> str:
        content = self.page.content()
        for kw in ("查看品牌", "新增品牌", "编辑品牌"):
            if kw in content:
                return kw
        return ""

    # ================================================================
    # 查看页内容读取
    # ================================================================

    def view_page_has_text(self, text: str) -> bool:
        return self.page.locator(f'text="{text}"').count() > 0

    # ================================================================
    # 标签页切换（基础信息 / 服务记录 / 已关联规格 / 余额修改记录）
    # ================================================================

    def click_view_tab(self, tab_name: str):
        self.page.locator(f'.el-tabs__item:has-text("{tab_name}")').click()
        self.page.wait_for_timeout(1000)

    def is_tab_active(self, tab_name: str) -> bool:
        tab = self.page.locator(f'.el-tabs__item:has-text("{tab_name}")')
        return tab.count() > 0 and "is-active" in (tab.get_attribute("class") or "")

    # ================================================================
    # 操作按钮
    # ================================================================

    def click_modify_agent_btn(self):
        self.page.locator('button:has-text("修改经纪人")').click()
        self.page.wait_for_timeout(1000)

    def click_edit_account_btn(self):
        self.page.locator('button:has-text("新增编辑账号密码")').click()
        self.page.wait_for_timeout(1000)

    def click_return_btn(self):
        self.page.locator('button:has-text("返回")').click()
        self.page.wait_for_timeout(1000)

    def has_dialog_visible(self) -> bool:
        return self.page.locator('.el-dialog:visible, .el-dialog__wrapper:visible').count() > 0

    def close_dialog(self):
        try:
            btn = self.page.locator('.el-dialog:visible .el-dialog__headerbtn')
            if btn.count() > 0:
                btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    # ================================================================
    # 列表页辅助（从列表进入查看、Tab 筛选等）
    # ================================================================

    def click_tab(self, tab_text: str):
        self.page.locator(f'.el-tabs__item:has-text("{tab_text}")').click()
        self.page.wait_for_timeout(1500)

    def get_list_row_count(self) -> int:
        self.page.wait_for_timeout(500)
        return self.page.locator('.el-table__body .el-table__row').count()

    def click_first_view_btn(self):
        self.page.locator('button:has-text("查看")').first.click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_view_by_name(self, brand_name: str):
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("查看")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)
