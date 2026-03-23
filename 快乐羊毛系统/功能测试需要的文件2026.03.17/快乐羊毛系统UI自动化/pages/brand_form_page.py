"""品牌表单页 Page Object（新增 & 编辑共用）

对应页面：#/coach/manage/edit?isEdit=1
新增品牌和编辑品牌共用同一个表单，所以放在一个类里。
  - test_brand_add.py  使用本类
  - test_brand_edit.py 使用本类
"""
from pages.base_page import BasePage


class BrandFormPage(BasePage):

    # ---- 表单字段选择器 ----
    SEL_BRAND_NAME = 'input[placeholder="请输入品牌名称"]'
    SEL_BRAND_CONTACT = 'input[placeholder="请输入品牌联系人手机号"]'
    SEL_CATEGORY_TYPE = '.el-form-item:has(.el-form-item__label:has-text("分类类型")) .el-select'
    SEL_API_CHANNEL = '.el-form-item:has(.el-form-item__label:has-text("接口渠道")) .el-select'
    SEL_CITY_SELECT = '.el-form-item:has(.el-form-item__label:has-text("品牌上架城市")) .el-select'
    SEL_COMMISSION_RATE = 'input[placeholder="请输入提成比例"]'
    SEL_DATE_START = '.el-form-item:has(.el-form-item__label:has-text("提成限期日期")) input:first-of-type'
    SEL_DATE_END = '.el-form-item:has(.el-form-item__label:has-text("提成限期日期")) input:last-of-type'
    SEL_BRAND_DESC = 'textarea[placeholder="请输入品牌简介"]'
    SEL_BRAND_ICON_UPLOAD = '.el-form-item:has(.el-form-item__label:has-text("品牌ICON")) .upload-container .img-wrap'
    SEL_BRAND_IMAGE_UPLOAD = '.el-form-item:has(.el-form-item__label:has-text("品牌图片")) .upload-container .img-wrap'
    SEL_BRAND_VIDEO_BTN = '.el-form-item:has(.el-form-item__label:has-text("品牌视频")) button:has-text("选择")'
    SEL_VIRTUAL_ORDERS = 'input[placeholder="请输入虚拟订单量"]'
    SEL_SOLD_OUT_YES = '.el-radio:has(.el-radio__label:has-text("售罄")):not(:has-text("未售罄"))'
    SEL_SOLD_OUT_NO = '.el-radio:has(.el-radio__label:has-text("未售罄"))'
    SEL_SUBMIT_BTN = '.el-form button:has-text("提交")'
    SEL_BACK_BTN = '.el-form button:has-text("返回")'

    # ---- 反馈提示 ----
    SEL_SUCCESS_MSG = '.el-message--success, .el-notification__content:has-text("成功")'
    SEL_ERROR_MSG = '.el-message--error, .el-message--warning, .el-notification__content'
    SEL_FORM_ERROR = '.el-form-item__error'

    # ---- 字符计数 ----
    SEL_NAME_COUNT = '.el-form-item:has(.el-form-item__label:has-text("品牌名称")) .el-input__suffix-inner'
    SEL_CONTACT_COUNT = '.el-form-item:has(.el-form-item__label:has-text("品牌联系人")) .el-input__suffix-inner'
    SEL_DESC_COUNT = '.el-form-item:has(.el-form-item__label:has-text("品牌简介")) .el-input__count-inner, .el-form-item:has(.el-form-item__label:has-text("品牌简介")) .el-textarea__count-inner'

    # ================================================================
    # 导航
    # ================================================================

    def goto_brand_list(self):
        from config.settings import BASE_URL
        self.page.goto(f"{BASE_URL.rstrip('/')}/#/coach/manage", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def goto_add_brand(self):
        """从列表页点击"新增品牌"进入空表单"""
        self.goto_brand_list()
        self._dismiss_notification()
        self.page.locator('button:has-text("新增品牌")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.page.wait_for_selector(self.SEL_BRAND_NAME, state="visible", timeout=10000)

    def goto_edit_brand(self, brand_name: str):
        """从列表页点击指定品牌的"编辑"按钮进入编辑表单"""
        self.goto_brand_list()
        self._dismiss_notification()
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.page.wait_for_selector(self.SEL_BRAND_NAME, state="visible", timeout=10000)

    def _dismiss_notification(self):
        try:
            btn = self.page.locator('button:has-text("忽 略"), button:has-text("忽略")')
            if btn.count() > 0:
                btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    # ================================================================
    # 填写表单
    # ================================================================

    def fill_brand_name(self, value: str):
        self.page.locator(self.SEL_BRAND_NAME).fill(value)

    def fill_brand_contact(self, value: str):
        self.page.locator(self.SEL_BRAND_CONTACT).fill(value)

    def fill_commission_rate(self, value: str):
        self.page.locator(self.SEL_COMMISSION_RATE).fill(value)

    def fill_brand_desc(self, value: str):
        self.page.locator(self.SEL_BRAND_DESC).fill(value)

    def fill_virtual_orders(self, value: str):
        self.page.locator(self.SEL_VIRTUAL_ORDERS).fill(value)

    def clear_and_fill_brand_name(self, value: str):
        self.page.locator(self.SEL_BRAND_NAME).fill("")
        self.page.locator(self.SEL_BRAND_NAME).fill(value)

    def clear_and_fill_brand_contact(self, value: str):
        self.page.locator(self.SEL_BRAND_CONTACT).fill("")
        self.page.locator(self.SEL_BRAND_CONTACT).fill(value)

    def clear_and_fill_commission_rate(self, value: str):
        self.page.locator(self.SEL_COMMISSION_RATE).fill("")
        self.page.locator(self.SEL_COMMISSION_RATE).fill(value)

    def clear_and_fill_brand_desc(self, value: str):
        self.page.locator(self.SEL_BRAND_DESC).fill("")
        self.page.locator(self.SEL_BRAND_DESC).fill(value)

    def clear_and_fill_virtual_orders(self, value: str):
        self.page.locator(self.SEL_VIRTUAL_ORDERS).fill("")
        self.page.locator(self.SEL_VIRTUAL_ORDERS).fill(value)

    def _select_dropdown(self, selector: str, index: int = 0):
        self.page.locator(selector).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def select_city(self, index: int = 0):
        self._select_dropdown(self.SEL_CITY_SELECT, index)

    def select_category_type(self, index: int = 0):
        self._select_dropdown(self.SEL_CATEGORY_TYPE, index)

    def select_api_channel(self, index: int = 0):
        self._select_dropdown(self.SEL_API_CHANNEL, index)

    def select_sold_out(self, sold_out: bool = True):
        sel = self.SEL_SOLD_OUT_YES if sold_out else self.SEL_SOLD_OUT_NO
        self.page.locator(sel).click()

    def upload_brand_icon(self, file_path: str):
        with self.page.expect_file_chooser() as fc:
            self.page.locator(self.SEL_BRAND_ICON_UPLOAD).click()
        fc.value.set_files(file_path)
        self.page.wait_for_timeout(2000)

    def upload_brand_image(self, file_path: str):
        with self.page.expect_file_chooser() as fc:
            self.page.locator(self.SEL_BRAND_IMAGE_UPLOAD).click()
        fc.value.set_files(file_path)
        self.page.wait_for_timeout(2000)

    def upload_brand_video(self, file_path: str):
        with self.page.expect_file_chooser() as fc:
            self.page.locator(self.SEL_BRAND_VIDEO_BTN).click()
        fc.value.set_files(file_path)
        self.page.wait_for_timeout(3000)

    def set_commission_date(self, start_date: str, end_date: str):
        start_input = self.page.locator(self.SEL_DATE_START)
        start_input.click()
        start_input.fill(start_date)
        end_input = self.page.locator(self.SEL_DATE_END)
        end_input.click()
        end_input.fill(end_date)
        end_input.press("Enter")
        self.page.wait_for_timeout(500)

    def fill_all_required(self, icon_path: str, image_path: str,
                          brand_name: str = "自动化测试品牌",
                          contact: str = "13800138000",
                          desc: str = "这是一个自动化测试品牌",
                          virtual_orders: str = "100"):
        self.fill_brand_name(brand_name)
        self.fill_brand_contact(contact)
        self.select_city()
        self.fill_brand_desc(desc)
        self.upload_brand_icon(icon_path)
        self.upload_brand_image(image_path)
        self.fill_virtual_orders(virtual_orders)
        self.select_sold_out(sold_out=False)

    def fill_required_except(self, skip_field: str, icon_path: str, image_path: str):
        fields = {
            "brand_name": ("自动化测试品牌", self.fill_brand_name),
            "contact": ("13800138000", self.fill_brand_contact),
            "city": (None, lambda _: self.select_city()),
            "desc": ("这是一个自动化测试品牌", self.fill_brand_desc),
            "icon": (icon_path, self.upload_brand_icon),
            "image": (image_path, self.upload_brand_image),
            "virtual_orders": ("100", self.fill_virtual_orders),
            "sold_out": (False, lambda v: self.select_sold_out(v)),
        }
        for name, (value, fn) in fields.items():
            if name != skip_field:
                fn(value)

    # ================================================================
    # 提交 & 返回
    # ================================================================

    def click_submit(self):
        self.page.locator(self.SEL_SUBMIT_BTN).click()
        self.page.wait_for_timeout(1000)

    def click_back(self):
        self.page.locator(self.SEL_BACK_BTN).click()
        self.page.wait_for_timeout(1000)

    # ================================================================
    # 断言辅助
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
            elements = self.page.locator(self.SEL_ERROR_MSG).all()
            return " ".join(el.text_content() or "" for el in elements).strip()
        except Exception:
            return ""

    def get_form_errors(self) -> list[str]:
        self.page.wait_for_timeout(500)
        errors = self.page.locator(self.SEL_FORM_ERROR).all()
        return [e.text_content().strip() for e in errors if e.text_content()]

    def has_form_error(self, keyword: str = "") -> bool:
        errors = self.get_form_errors()
        if not keyword:
            return len(errors) > 0
        return any(keyword in e for e in errors)

    def get_field_error(self, field_label: str) -> str:
        sel = f'.el-form-item:has(.el-form-item__label:has-text("{field_label}")) .el-form-item__error'
        try:
            el = self.page.locator(sel)
            if el.count() > 0:
                return el.first.text_content().strip()
        except Exception:
            pass
        return ""

    def is_on_brand_list(self) -> bool:
        return "/coach/manage" in self.current_url and "/edit" not in self.current_url

    def is_on_edit_page(self) -> bool:
        return "/coach/manage/edit" in self.current_url and "isEdit=0" not in self.current_url

    def get_view_title(self) -> str:
        content = self.page.content()
        for kw in ("查看品牌", "新增品牌", "编辑品牌"):
            if kw in content:
                return kw
        return ""

    def get_brand_name_value(self) -> str:
        return self.page.locator(self.SEL_BRAND_NAME).input_value()

    def get_brand_name_count(self) -> str:
        try:
            return self.page.locator(self.SEL_NAME_COUNT).text_content().strip()
        except Exception:
            return ""

    def get_brand_contact_count(self) -> str:
        try:
            return self.page.locator(self.SEL_CONTACT_COUNT).text_content().strip()
        except Exception:
            return ""

    def get_brand_desc_count(self) -> str:
        try:
            return self.page.locator(self.SEL_DESC_COUNT).text_content().strip()
        except Exception:
            return ""

    def is_submit_button_enabled(self) -> bool:
        return self.page.locator(self.SEL_SUBMIT_BTN).is_enabled()

    def has_icon_preview(self) -> bool:
        return self.page.locator('.el-form-item:has(.el-form-item__label:has-text("品牌ICON")) .upload-container img').count() > 0

    def has_image_preview(self) -> bool:
        return self.page.locator('.el-form-item:has(.el-form-item__label:has-text("品牌图片")) .upload-container img').count() > 0

    def brand_exists_in_list(self, brand_name: str) -> bool:
        self.page.wait_for_timeout(1000)
        return self.page.locator(f'text="{brand_name}"').count() > 0

    def get_list_brand_names(self) -> list[str]:
        self.page.wait_for_timeout(500)
        cells = self.page.locator('.el-table__body .el-table__row td:nth-child(3)').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def click_edit_by_name(self, brand_name: str):
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_view_tab(self, tab_name: str):
        self.page.locator(f'.el-tabs__item:has-text("{tab_name}")').click()
        self.page.wait_for_timeout(1000)

    def is_tab_active(self, tab_name: str) -> bool:
        tab = self.page.locator(f'.el-tabs__item:has-text("{tab_name}")')
        return tab.count() > 0 and "is-active" in (tab.get_attribute("class") or "")

    def click_modify_agent_btn(self):
        self.page.locator('button:has-text("修改经纪人")').click()
        self.page.wait_for_timeout(1000)

    def click_edit_account_btn(self):
        self.page.locator('button:has-text("新增编辑账号密码")').click()
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
