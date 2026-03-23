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
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")').first
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_view_by_name(self, brand_name: str):
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")').first
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

    # ================================================================
    # 更多菜单（品牌删除通过此菜单操作）
    # ================================================================

    def click_more_menu_by_name(self, brand_name: str):
        """点击指定品牌的"更多菜单"按钮"""
        # 遍历每行的所有 td，找到文本完全等于品牌名的行
        rows = self.page.locator('.el-table__body .el-table__row').all()
        for row in rows:
            cells = row.locator('td').all()
            for cell in cells:
                if cell.text_content().strip() == brand_name:
                    row.locator('button:has-text("更多菜单")').click()
                    self.page.wait_for_timeout(1500)
                    return
        # 没找到精确匹配，用第一个包含该名称的行
        self.page.locator('button:has-text("更多菜单")').first.click()
        self.page.wait_for_timeout(1500)

    def click_more_menu_first(self):
        """点击列表中第一个"更多菜单"按钮"""
        self.page.locator('button:has-text("更多菜单")').first.click()
        self.page.wait_for_timeout(1500)

    def get_dropdown_items(self) -> list[str]:
        """获取当前展开的下拉菜单所有选项文本"""
        items = self.page.locator('.el-dropdown-menu__item:visible').all()
        return [item.text_content().strip() for item in items if item.text_content()]

    def click_dropdown_item(self, item_text: str):
        """点击下拉菜单中的指定选项"""
        self.page.locator(f'.el-dropdown-menu__item:visible:has-text("{item_text}")').click()
        self.page.wait_for_timeout(800)

    def dismiss_dropdown(self):
        """关闭下拉菜单"""
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(800)

    def is_dropdown_visible(self) -> bool:
        return self.page.locator('.el-dropdown-menu__item:visible').count() > 0

    # ================================================================
    # 删除确认弹窗
    # ================================================================

    SEL_MSG_BOX = '.el-message-box:visible'
    SEL_MSG_BOX_TITLE = '.el-message-box:visible .el-message-box__title'
    SEL_MSG_BOX_CONTENT = '.el-message-box:visible .el-message-box__message'
    SEL_MSG_BOX_OK = '.el-message-box:visible button:has-text("确认"), .el-message-box:visible button:has-text("确定")'
    SEL_MSG_BOX_CANCEL = '.el-message-box:visible button:has-text("取消")'
    SEL_MSG_BOX_CLOSE = '.el-message-box:visible .el-message-box__headerbtn'
    SEL_SUCCESS_MSG = '.el-message--success'
    SEL_ERROR_MSG = '.el-message--error, .el-message--warning'

    def delete_brand_by_name(self, brand_name: str):
        """通过更多菜单点击删除（不点确认）"""
        self.click_more_menu_by_name(brand_name)
        self.click_dropdown_item("删除")

    def is_msgbox_visible(self) -> bool:
        return self.page.locator(self.SEL_MSG_BOX).count() > 0

    def get_msgbox_title(self) -> str:
        try:
            return self.page.locator(self.SEL_MSG_BOX_TITLE).text_content().strip()
        except Exception:
            return ""

    def get_msgbox_content(self) -> str:
        try:
            return self.page.locator(self.SEL_MSG_BOX_CONTENT).text_content().strip()
        except Exception:
            return ""

    def click_msgbox_ok(self):
        self.page.locator(self.SEL_MSG_BOX_OK).click()
        self.page.wait_for_timeout(1500)

    def click_msgbox_cancel(self):
        self.page.locator(self.SEL_MSG_BOX_CANCEL).click()
        self.page.wait_for_timeout(500)

    def click_msgbox_close_x(self):
        self.page.locator(self.SEL_MSG_BOX_CLOSE).click()
        self.page.wait_for_timeout(500)

    def dismiss_msgbox_by_esc(self):
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def get_success_message(self, timeout: int = 5000) -> str:
        try:
            self.page.wait_for_selector(self.SEL_SUCCESS_MSG, timeout=timeout)
            return self.page.locator(self.SEL_SUCCESS_MSG).first.text_content() or ""
        except Exception:
            return ""

    def get_error_message(self, timeout: int = 3000) -> str:
        try:
            self.page.wait_for_selector(self.SEL_ERROR_MSG, timeout=timeout)
            return self.page.locator(self.SEL_ERROR_MSG).first.text_content() or ""
        except Exception:
            return ""

    def brand_exists(self, brand_name: str) -> bool:
        self.page.wait_for_timeout(500)
        return brand_name in self.get_list_brand_names()
