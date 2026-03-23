"""品牌列表页 Page Object（搜索 & 筛选 & 分页）

对应页面：#/coach/manage
  - test_brand_search.py 使用本类
"""
from pages.base_page import BasePage


class BrandListPage(BasePage):

    # ---- 搜索区选择器 ----
    SEL_SEARCH_INPUT = 'input[placeholder="输入查询"]'
    SEL_SEARCH_BTN = 'button:has-text("搜索")'
    SEL_RESET_BTN = 'button:has-text("重置")'
    SEL_AGENT_SELECT = '.el-form-item:has-text("品牌所属代理商") .el-select'
    SEL_DATE_START = '.el-form-item:has-text("申请时间") input:first-of-type'
    SEL_DATE_END = '.el-form-item:has-text("申请时间") input:last-of-type'
    SEL_CITY_FILTER = '.el-form-item:has-text("选择品牌上架城市") .el-select'

    # ================================================================
    # 导航
    # ================================================================

    def goto_brand_list(self):
        from config.settings import BASE_URL
        self.page.goto(f"{BASE_URL.rstrip('/')}/#/coach/manage", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def _dismiss_notification(self):
        try:
            btn = self.page.locator('button:has-text("忽 略"), button:has-text("忽略")')
            if btn.count() > 0:
                btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    # ================================================================
    # 搜索 & 筛选
    # ================================================================

    def search_by_keyword(self, keyword: str):
        self.page.locator(self.SEL_SEARCH_INPUT).fill(keyword)
        self.page.locator(self.SEL_SEARCH_BTN).click()
        self.page.wait_for_timeout(1500)

    def click_search(self):
        self.page.locator(self.SEL_SEARCH_BTN).click()
        self.page.wait_for_timeout(1500)

    def click_reset(self):
        self.page.locator(self.SEL_RESET_BTN).click()
        self.page.wait_for_timeout(1500)

    def get_search_input_value(self) -> str:
        return self.page.locator(self.SEL_SEARCH_INPUT).input_value()

    def select_agent_filter(self, index: int = 0):
        self.page.locator(self.SEL_AGENT_SELECT).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def select_city_filter(self, city_name: str = ""):
        self.page.locator(self.SEL_CITY_FILTER).click()
        self.page.wait_for_timeout(500)
        if city_name:
            option = self.page.locator(f'.el-select-dropdown:visible .el-select-dropdown__item:has-text("{city_name}")')
            if option.count() > 0:
                option.first.click()
            else:
                self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item').first.click()
        else:
            self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item').first.click()
        self.page.wait_for_timeout(300)

    def set_apply_date_range(self, start: str, end: str):
        start_input = self.page.locator(self.SEL_DATE_START)
        start_input.click()
        start_input.fill(start)
        end_input = self.page.locator(self.SEL_DATE_END)
        end_input.click()
        end_input.fill(end)
        end_input.press("Enter")
        self.page.wait_for_timeout(500)

    # ================================================================
    # Tab 状态筛选
    # ================================================================

    def click_tab(self, tab_text: str):
        self.page.locator(f'.el-tabs__item:has-text("{tab_text}")').click()
        self.page.wait_for_timeout(1500)

    def get_tab_text(self, tab_text: str) -> str:
        try:
            return self.page.locator(f'.el-tabs__item:has-text("{tab_text}")').text_content().strip()
        except Exception:
            return ""

    # ================================================================
    # 列表数据读取
    # ================================================================

    def get_list_brand_names(self) -> list[str]:
        self.page.wait_for_timeout(500)
        cells = self.page.locator('.el-table__body .el-table__row td:nth-child(3)').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def get_list_row_count(self) -> int:
        self.page.wait_for_timeout(500)
        return self.page.locator('.el-table__body .el-table__row').count()

    def get_list_column_texts(self, col_index: int) -> list[str]:
        self.page.wait_for_timeout(500)
        cells = self.page.locator(f'.el-table__body .el-table__row td:nth-child({col_index})').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def get_list_headers(self) -> list[str]:
        headers = self.page.locator('.el-table__header th .cell').all()
        return [h.text_content().strip() for h in headers if h.text_content()]

    def get_list_total_text(self) -> str:
        try:
            return self.page.locator('.el-pagination__total, text=/共.*条/').first.text_content().strip()
        except Exception:
            return ""

    def is_list_empty(self) -> bool:
        empty = self.page.locator('.el-table__empty-text, text="暂无数据"')
        return empty.count() > 0 or self.get_list_row_count() == 0

    def is_on_brand_list(self) -> bool:
        return "/coach/manage" in self.current_url and "/edit" not in self.current_url

    # ================================================================
    # 列表操作按钮
    # ================================================================

    def click_edit_by_name(self, brand_name: str):
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_view_by_name(self, brand_name: str):
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("查看")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_first_view_btn(self):
        self.page.locator('button:has-text("查看")').first.click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    # ================================================================
    # 分页
    # ================================================================

    def click_next_page(self):
        self.page.locator('button:has-text("下一页"), .btn-next').click()
        self.page.wait_for_timeout(1500)
