"""渠道管理页 Page Object

对应页面：#/coach/coachLabel
渠道管理的新增/编辑通过弹窗操作（只有一个名称输入框 maxlength=10），删除通过确认弹窗。
  - test_channel_add.py    使用本类
  - test_channel_edit.py   使用本类
  - test_channel_delete.py 使用本类
"""
from pages.base_page import BasePage


class ChannelPage(BasePage):

    # ---- 列表页 ----
    SEL_ADD_BTN = 'button:has-text("新增渠道")'

    # ---- 弹窗表单（新增 & 编辑共用） ----
    SEL_DIALOG = '.el-dialog:visible'
    SEL_DIALOG_TITLE = '.el-dialog:visible .el-dialog__header'
    SEL_DIALOG_CLOSE = '.el-dialog:visible .el-dialog__headerbtn'
    SEL_CHANNEL_NAME = '.el-dialog:visible input[placeholder="请输入标签名称"]'
    SEL_NAME_COUNT = '.el-dialog:visible .el-input__count-inner, .el-dialog:visible .el-input__suffix-inner'
    SEL_CLOSE_BTN = '.el-dialog:visible button:has-text("关闭")'
    SEL_CONFIRM_BTN = '.el-dialog:visible button:has-text("确认")'

    # ---- 反馈提示 ----
    SEL_SUCCESS_MSG = '.el-message--success'
    SEL_ERROR_MSG = '.el-message--error, .el-message--warning'
    SEL_FORM_ERROR = '.el-dialog:visible .el-form-item__error'

    # ---- 删除确认弹窗 ----
    SEL_MSG_BOX = '.el-message-box:visible'
    SEL_MSG_BOX_TITLE = '.el-message-box:visible .el-message-box__title'
    SEL_MSG_BOX_CONTENT = '.el-message-box:visible .el-message-box__message'
    SEL_MSG_BOX_OK = '.el-message-box:visible button:has-text("确定")'
    SEL_MSG_BOX_CANCEL = '.el-message-box:visible button:has-text("取消")'

    # ================================================================
    # 导航
    # ================================================================

    def goto_channel_list(self):
        from config.settings import BASE_URL
        self.page.goto(f"{BASE_URL.rstrip('/')}/#/coach/coachLabel", wait_until="domcontentloaded")
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
        self.page.locator(self.SEL_ADD_BTN).click()
        self.page.wait_for_selector(self.SEL_DIALOG, state="visible", timeout=5000)

    def click_edit_by_name(self, name: str):
        row = self.page.locator(f'.el-table__row:has-text("{name}")').first
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_selector(self.SEL_DIALOG, state="visible", timeout=5000)

    def click_delete_by_name(self, name: str):
        row = self.page.locator(f'.el-table__row:has-text("{name}")').first
        row.locator('button:has-text("删除")').click()
        self.page.wait_for_timeout(800)

    def is_dialog_visible(self) -> bool:
        return self.page.locator(self.SEL_DIALOG).count() > 0

    def get_dialog_title(self) -> str:
        try:
            return self.page.locator(self.SEL_DIALOG_TITLE).text_content().strip()
        except Exception:
            return ""

    def click_dialog_close_x(self):
        self.page.locator(self.SEL_DIALOG_CLOSE).click()
        self.page.wait_for_timeout(500)

    # ================================================================
    # 表单
    # ================================================================

    def fill_channel_name(self, value: str):
        self.page.locator(self.SEL_CHANNEL_NAME).fill(value)

    def clear_and_fill_channel_name(self, value: str):
        self.page.locator(self.SEL_CHANNEL_NAME).fill("")
        self.page.locator(self.SEL_CHANNEL_NAME).fill(value)

    def get_channel_name_value(self) -> str:
        return self.page.locator(self.SEL_CHANNEL_NAME).input_value()

    def get_name_count(self) -> str:
        try:
            return self.page.locator(self.SEL_NAME_COUNT).text_content().strip()
        except Exception:
            return ""

    def click_confirm(self):
        self.page.locator(self.SEL_CONFIRM_BTN).click()
        self.page.wait_for_timeout(1000)

    def click_close(self):
        self.page.locator(self.SEL_CLOSE_BTN).click()
        self.page.wait_for_timeout(500)

    # ================================================================
    # 删除确认弹窗
    # ================================================================

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
        self.page.wait_for_timeout(1000)

    def click_msgbox_cancel(self):
        self.page.locator(self.SEL_MSG_BOX_CANCEL).click()
        self.page.wait_for_timeout(500)

    def dismiss_msgbox_by_esc(self):
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    # ================================================================
    # 列表数据
    # ================================================================

    def get_list_names(self) -> list[str]:
        self.page.wait_for_timeout(500)
        cells = self.page.locator('.el-table__body .el-table__row td:nth-child(2)').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def get_list_row_count(self) -> int:
        self.page.wait_for_timeout(500)
        return self.page.locator('.el-table__body .el-table__row').count()

    def channel_exists(self, name: str) -> bool:
        self.page.wait_for_timeout(500)
        return name in self.get_list_names()

    def get_list_total_text(self) -> str:
        try:
            return self.page.locator('.el-pagination__total, text=/共.*条/').first.text_content().strip()
        except Exception:
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
