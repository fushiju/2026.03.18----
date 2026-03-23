"""品牌分类页 Page Object

对应页面：#/coach/category
品牌分类的新增/编辑通过弹窗操作，删除通过确认弹窗操作。
  - test_category_add.py    使用本类
  - test_category_edit.py   使用本类
  - test_category_delete.py 使用本类
"""
from pages.base_page import BasePage


class BrandCategoryPage(BasePage):

    # ---- 列表页 ----
    SEL_ADD_BTN = 'button:has-text("新增模块")'

    # ---- 弹窗表单（新增 & 编辑共用） ----
    SEL_DIALOG = '.el-dialog:visible'
    SEL_DIALOG_TITLE = '.el-dialog:visible .el-dialog__header'
    SEL_DIALOG_CLOSE = '.el-dialog:visible .el-dialog__headerbtn'
    SEL_CATEGORY_TYPE = '.el-dialog:visible .el-form-item:has(.el-form-item__label:has-text("分类类型")) .el-select'
    SEL_CATEGORY_NAME = '.el-dialog:visible input[placeholder="请输入分类名称"]'
    SEL_LEVEL_INPUT = '.el-dialog:visible .el-input-number input'
    SEL_LEVEL_INCREASE = '.el-dialog:visible .el-input-number .el-input-number__increase, .el-dialog:visible button:has-text("增加数值")'
    SEL_LEVEL_DECREASE = '.el-dialog:visible .el-input-number .el-input-number__decrease, .el-dialog:visible button:has-text("减少数值")'
    SEL_STATUS_SWITCH = '.el-dialog:visible .el-switch'
    SEL_CANCEL_BTN = '.el-dialog:visible button:has-text("取消")'
    SEL_SUBMIT_BTN = '.el-dialog:visible button:has-text("提交")'

    # ---- 反馈提示 ----
    SEL_SUCCESS_MSG = '.el-message--success'
    SEL_ERROR_MSG = '.el-message--error, .el-message--warning'
    SEL_FORM_ERROR = '.el-dialog:visible .el-form-item__error'

    # ---- 删除确认弹窗 ----
    SEL_CONFIRM_DIALOG = '.el-message-box:visible'
    SEL_CONFIRM_TITLE = '.el-message-box:visible .el-message-box__title'
    SEL_CONFIRM_CONTENT = '.el-message-box:visible .el-message-box__message'
    SEL_CONFIRM_OK = '.el-message-box:visible button:has-text("确定")'
    SEL_CONFIRM_CANCEL = '.el-message-box:visible button:has-text("取消")'
    SEL_CONFIRM_CLOSE = '.el-message-box:visible .el-message-box__headerbtn'

    # ================================================================
    # 导航
    # ================================================================

    def goto_category_list(self):
        from config.settings import BASE_URL
        self.page.goto(f"{BASE_URL.rstrip('/')}/#/coach/category", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self._dismiss_notification()

    def _dismiss_notification(self):
        try:
            btn = self.page.locator('button:has-text("忽 略"), button:has-text("忽略")')
            if btn.count() > 0:
                btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    # ================================================================
    # 弹窗操作
    # ================================================================

    def click_add_btn(self):
        """点击"新增模块"按钮，打开新增弹窗"""
        self.page.locator(self.SEL_ADD_BTN).click()
        self.page.wait_for_timeout(800)

    def click_edit_by_name(self, name: str):
        """点击指定分类的"编辑"按钮"""
        row = self.page.locator(f'.el-table__row:has-text("{name}")')
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_timeout(800)

    def click_delete_by_name(self, name: str):
        """点击指定分类的"删除"按钮"""
        row = self.page.locator(f'.el-table__row:has-text("{name}")')
        row.locator('button:has-text("删除")').click()
        self.page.wait_for_timeout(800)

    def is_dialog_visible(self) -> bool:
        return self.page.locator(self.SEL_DIALOG).count() > 0

    def get_dialog_title(self) -> str:
        try:
            return self.page.locator(self.SEL_DIALOG_TITLE).text_content().strip()
        except Exception:
            return ""

    def click_dialog_close(self):
        """点击弹窗右上角X关闭"""
        self.page.locator(self.SEL_DIALOG_CLOSE).click()
        self.page.wait_for_timeout(500)

    # ================================================================
    # 表单填写
    # ================================================================

    def fill_category_name(self, value: str):
        self.page.locator(self.SEL_CATEGORY_NAME).fill(value)

    def clear_and_fill_category_name(self, value: str):
        self.page.locator(self.SEL_CATEGORY_NAME).fill("")
        self.page.locator(self.SEL_CATEGORY_NAME).fill(value)

    def get_category_name_value(self) -> str:
        return self.page.locator(self.SEL_CATEGORY_NAME).input_value()

    def select_category_type(self, index: int = 0):
        self.page.locator(self.SEL_CATEGORY_TYPE).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def fill_level(self, value: str):
        inp = self.page.locator(self.SEL_LEVEL_INPUT)
        inp.click()
        inp.fill(value)

    def get_level_value(self) -> str:
        return self.page.locator(self.SEL_LEVEL_INPUT).input_value()

    def click_level_increase(self):
        self.page.locator(self.SEL_LEVEL_INCREASE).click()
        self.page.wait_for_timeout(200)

    def click_level_decrease(self):
        self.page.locator(self.SEL_LEVEL_DECREASE).click()
        self.page.wait_for_timeout(200)

    def is_status_enabled(self) -> bool:
        """分类状态开关是否为启用"""
        sw = self.page.locator(self.SEL_STATUS_SWITCH)
        return "is-checked" in (sw.get_attribute("class") or "")

    def toggle_status(self):
        """切换分类状态开关"""
        self.page.locator(self.SEL_STATUS_SWITCH).click()
        self.page.wait_for_timeout(300)

    def click_submit(self):
        self.page.locator(self.SEL_SUBMIT_BTN).click()
        self.page.wait_for_timeout(1000)

    def click_cancel(self):
        self.page.locator(self.SEL_CANCEL_BTN).click()
        self.page.wait_for_timeout(500)

    # ================================================================
    # 删除确认弹窗
    # ================================================================

    def is_confirm_visible(self) -> bool:
        return self.page.locator(self.SEL_CONFIRM_DIALOG).count() > 0

    def get_confirm_title(self) -> str:
        try:
            return self.page.locator(self.SEL_CONFIRM_TITLE).text_content().strip()
        except Exception:
            return ""

    def get_confirm_content(self) -> str:
        try:
            return self.page.locator(self.SEL_CONFIRM_CONTENT).text_content().strip()
        except Exception:
            return ""

    def click_confirm_ok(self):
        self.page.locator(self.SEL_CONFIRM_OK).click()
        self.page.wait_for_timeout(1000)

    def click_confirm_cancel(self):
        self.page.locator(self.SEL_CONFIRM_CANCEL).click()
        self.page.wait_for_timeout(500)

    def click_confirm_close(self):
        self.page.locator(self.SEL_CONFIRM_CLOSE).click()
        self.page.wait_for_timeout(500)

    # ================================================================
    # 列表数据读取
    # ================================================================

    def get_list_names(self) -> list[str]:
        """获取所有分类名称"""
        self.page.wait_for_timeout(500)
        cells = self.page.locator('.el-table__body .el-table__row td:nth-child(3)').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def get_list_row_count(self) -> int:
        self.page.wait_for_timeout(500)
        return self.page.locator('.el-table__body .el-table__row').count()

    def category_exists(self, name: str) -> bool:
        self.page.wait_for_timeout(500)
        return name in self.get_list_names()

    def get_category_status(self, name: str) -> str:
        """获取指定分类的状态文本"""
        row = self.page.locator(f'.el-table__row:has-text("{name}")')
        # 状态列是第4列（ID, 展开, 分类名称, 分类状态）
        cells = row.locator('td').all()
        for cell in cells:
            text = cell.text_content().strip()
            if text in ("启用", "禁用"):
                return text
        return ""

    def is_list_empty(self) -> bool:
        empty = self.page.locator('.el-table__empty-text, text="暂无数据"')
        return empty.count() > 0 or self.get_list_row_count() == 0

    # ================================================================
    # 反馈提示
    # ================================================================

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

    def get_form_errors(self) -> list[str]:
        self.page.wait_for_timeout(500)
        errors = self.page.locator(self.SEL_FORM_ERROR).all()
        return [e.text_content().strip() for e in errors if e.text_content()]

    def has_form_error(self) -> bool:
        return len(self.get_form_errors()) > 0
