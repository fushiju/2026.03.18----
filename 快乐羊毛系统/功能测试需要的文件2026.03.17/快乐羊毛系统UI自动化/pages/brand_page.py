"""品牌管理页 Page Object"""
import time
from pathlib import Path
from pages.base_page import BasePage


class BrandPage(BasePage):
    # ---- URL ----
    BRAND_LIST_URL = "#/coach/manage"
    BRAND_ADD_URL = "#/coach/manage/edit"

    # ---- 品牌列表页 ----
    SEL_ADD_BRAND_BTN = 'button:has-text("新增品牌")'
    SEL_SEARCH_INPUT = 'input[placeholder="输入查询"]'
    SEL_SEARCH_BTN = 'button:has-text("搜索")'
    SEL_RESET_BTN = 'button:has-text("重置")'

    # ---- 新增品牌表单 ----
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
    SEL_HIDE_SALES_CHECKBOX = '.el-checkbox:has-text("不显示实际销量")'
    SEL_SOLD_OUT_YES = '.el-radio:has(.el-radio__label:has-text("售罄")):not(:has-text("未售罄"))'
    SEL_SOLD_OUT_NO = '.el-radio:has(.el-radio__label:has-text("未售罄"))'
    SEL_SUBMIT_BTN = '.el-form button:has-text("提交")'
    SEL_BACK_BTN = '.el-form button:has-text("返回")'

    # ---- 通用反馈 ----
    SEL_SUCCESS_MSG = '.el-message--success, .el-notification__content:has-text("成功")'
    SEL_ERROR_MSG = '.el-message--error, .el-message--warning, .el-notification__content'
    SEL_FORM_ERROR = '.el-form-item__error'
    SEL_FORM_ITEM_ERROR = '.el-form-item.is-error'

    # ---- 字符计数 ----
    SEL_NAME_COUNT = '.el-form-item:has(.el-form-item__label:has-text("品牌名称")) .el-input__suffix-inner'
    SEL_CONTACT_COUNT = '.el-form-item:has(.el-form-item__label:has-text("品牌联系人")) .el-input__suffix-inner'
    SEL_DESC_COUNT = '.el-form-item:has(.el-form-item__label:has-text("品牌简介")) .el-input__count-inner, .el-form-item:has(.el-form-item__label:has-text("品牌简介")) .el-textarea__count-inner'

    # ==============================================================
    # 导航方法
    # ==============================================================

    def goto_brand_list(self):
        """导航到品牌管理列表页"""
        from config.settings import BASE_URL
        url = f"{BASE_URL.rstrip('/')}/{self.BRAND_LIST_URL}"
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def goto_add_brand(self):
        """从品牌列表页点击"新增品牌"按钮进入新增表单"""
        self.goto_brand_list()
        self._dismiss_notification()
        self.page.locator(self.SEL_ADD_BRAND_BTN).click()
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self.page.wait_for_selector(self.SEL_BRAND_NAME, state="visible", timeout=10000)

    def _dismiss_notification(self):
        """关闭可能弹出的通知弹窗"""
        try:
            ignore_btn = self.page.locator('button:has-text("忽 略"), button:has-text("忽略")')
            if ignore_btn.count() > 0:
                ignore_btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    # ==============================================================
    # 表单填写方法
    # ==============================================================

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

    def select_city(self, index: int = 0):
        """点击品牌上架城市下拉框并选择第 index 项"""
        self.page.locator(self.SEL_CITY_SELECT).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def select_category_type(self, index: int = 0):
        """选择分类类型"""
        self.page.locator(self.SEL_CATEGORY_TYPE).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def select_api_channel(self, index: int = 0):
        """选择接口渠道"""
        self.page.locator(self.SEL_API_CHANNEL).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def select_sold_out(self, sold_out: bool = True):
        """选择是否售罄"""
        if sold_out:
            self.page.locator(self.SEL_SOLD_OUT_YES).click()
        else:
            self.page.locator(self.SEL_SOLD_OUT_NO).click()

    def upload_brand_icon(self, file_path: str):
        """上传品牌 ICON 图片"""
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(self.SEL_BRAND_ICON_UPLOAD).click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)
        self.page.wait_for_timeout(2000)

    def upload_brand_image(self, file_path: str):
        """上传品牌图片"""
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(self.SEL_BRAND_IMAGE_UPLOAD).click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)
        self.page.wait_for_timeout(2000)

    def upload_brand_video(self, file_path: str):
        """上传品牌视频"""
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(self.SEL_BRAND_VIDEO_BTN).click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)
        self.page.wait_for_timeout(3000)

    def set_commission_date(self, start_date: str, end_date: str):
        """设置提成限期日期范围，格式 'YYYY-MM-DD'"""
        start_input = self.page.locator(self.SEL_DATE_START)
        start_input.click()
        start_input.fill(start_date)
        end_input = self.page.locator(self.SEL_DATE_END)
        end_input.click()
        end_input.fill(end_date)
        # 按 Enter 确认
        end_input.press("Enter")
        self.page.wait_for_timeout(500)

    def click_submit(self):
        """点击提交按钮"""
        self.page.locator(self.SEL_SUBMIT_BTN).click()
        self.page.wait_for_timeout(1000)

    def click_back(self):
        """点击返回按钮"""
        self.page.locator(self.SEL_BACK_BTN).click()
        self.page.wait_for_timeout(1000)

    # ==============================================================
    # 填写必填项辅助方法（用于需要跳过某个字段的测试）
    # ==============================================================

    def fill_all_required(self, icon_path: str, image_path: str,
                          brand_name: str = "自动化测试品牌",
                          contact: str = "13800138000",
                          desc: str = "这是一个自动化测试品牌",
                          virtual_orders: str = "100"):
        """填写所有必填字段（通用辅助方法）"""
        self.fill_brand_name(brand_name)
        self.fill_brand_contact(contact)
        self.select_city()
        self.fill_brand_desc(desc)
        self.upload_brand_icon(icon_path)
        self.upload_brand_image(image_path)
        self.fill_virtual_orders(virtual_orders)
        self.select_sold_out(sold_out=False)

    def fill_required_except(self, skip_field: str, icon_path: str, image_path: str):
        """填写除 skip_field 外的所有必填字段"""
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

    # ==============================================================
    # 断言辅助方法
    # ==============================================================

    def get_success_message(self, timeout: int = 5000) -> str:
        """获取成功提示信息"""
        try:
            self.page.wait_for_selector(self.SEL_SUCCESS_MSG, timeout=timeout)
            return self.page.locator(self.SEL_SUCCESS_MSG).first.text_content() or ""
        except Exception:
            return ""

    def get_error_message(self, timeout: int = 3000) -> str:
        """获取弹窗错误信息"""
        try:
            self.page.wait_for_selector(self.SEL_ERROR_MSG, timeout=timeout)
            elements = self.page.locator(self.SEL_ERROR_MSG).all()
            texts = [el.text_content() or "" for el in elements]
            return " ".join(texts).strip()
        except Exception:
            return ""

    def get_form_errors(self) -> list[str]:
        """获取所有表单校验错误提示"""
        self.page.wait_for_timeout(500)
        errors = self.page.locator(self.SEL_FORM_ERROR).all()
        return [e.text_content().strip() for e in errors if e.text_content()]

    def has_form_error(self, keyword: str = "") -> bool:
        """检查表单是否有校验错误，可选关键字过滤"""
        errors = self.get_form_errors()
        if not keyword:
            return len(errors) > 0
        return any(keyword in e for e in errors)

    def get_field_error(self, field_label: str) -> str:
        """获取指定字段的校验错误信息"""
        selector = f'.el-form-item:has(.el-form-item__label:has-text("{field_label}")) .el-form-item__error'
        try:
            el = self.page.locator(selector)
            if el.count() > 0:
                return el.first.text_content().strip()
        except Exception:
            pass
        return ""

    def is_on_brand_list(self) -> bool:
        """判断当前是否在品牌列表页"""
        return "/coach/manage" in self.current_url and "/edit" not in self.current_url

    def is_on_add_brand_page(self) -> bool:
        """判断当前是否在新增品牌页"""
        return "/coach/manage/edit" in self.current_url

    def get_brand_name_count(self) -> str:
        """获取品牌名称字符计数文本"""
        try:
            return self.page.locator(self.SEL_NAME_COUNT).text_content().strip()
        except Exception:
            return ""

    def get_brand_contact_count(self) -> str:
        """获取品牌联系人字符计数文本"""
        try:
            return self.page.locator(self.SEL_CONTACT_COUNT).text_content().strip()
        except Exception:
            return ""

    def get_brand_desc_count(self) -> str:
        """获取品牌简介字符计数文本"""
        try:
            return self.page.locator(self.SEL_DESC_COUNT).text_content().strip()
        except Exception:
            return ""

    def get_brand_name_value(self) -> str:
        """获取品牌名称输入框的值"""
        return self.page.locator(self.SEL_BRAND_NAME).input_value()

    def brand_exists_in_list(self, brand_name: str) -> bool:
        """检查品牌列表中是否存在指定品牌"""
        self.page.wait_for_timeout(1000)
        return self.page.locator(f'text="{brand_name}"').count() > 0

    def get_page_title(self) -> str:
        """获取页面标题文字（新增品牌 / 编辑品牌）"""
        try:
            # 面包屑最后一项 or 页面标题
            breadcrumb = self.page.locator('.el-breadcrumb__item:last-child')
            if breadcrumb.count() > 0:
                return breadcrumb.text_content().strip()
        except Exception:
            pass
        return ""

    def is_submit_button_enabled(self) -> bool:
        """检查提交按钮是否可点击"""
        return self.page.locator(self.SEL_SUBMIT_BTN).is_enabled()

    def has_icon_preview(self) -> bool:
        """检查品牌ICON是否有图片预览"""
        preview = self.page.locator(
            '.el-form-item:has(.el-form-item__label:has-text("品牌ICON")) .upload-container img'
        )
        return preview.count() > 0

    def has_image_preview(self) -> bool:
        """检查品牌图片是否有图片预览"""
        preview = self.page.locator(
            '.el-form-item:has(.el-form-item__label:has-text("品牌图片")) .upload-container img'
        )
        return preview.count() > 0

    # ==============================================================
    # 品牌列表页操作
    # ==============================================================

    def click_edit_by_name(self, brand_name: str):
        """在列表中找到指定品牌并点击"编辑"按钮"""
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("编辑")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_view_by_name(self, brand_name: str):
        """在列表中找到指定品牌并点击"查看"按钮"""
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")')
        row.locator('button:has-text("查看")').click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_first_edit_btn(self):
        """点击列表中第一个"编辑"按钮"""
        self.page.locator('button:has-text("编辑")').first.click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def click_first_view_btn(self):
        """点击列表中第一个"查看"按钮"""
        self.page.locator('button:has-text("查看")').first.click()
        self.page.wait_for_load_state("networkidle", timeout=15000)

    def get_list_brand_names(self) -> list[str]:
        """获取当前列表页所有品牌名称"""
        self.page.wait_for_timeout(500)
        # 品牌名称是表格第3列
        cells = self.page.locator('.el-table__body .el-table__row td:nth-child(3)').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def get_list_row_count(self) -> int:
        """获取当前列表行数"""
        self.page.wait_for_timeout(500)
        return self.page.locator('.el-table__body .el-table__row').count()

    def get_list_total_text(self) -> str:
        """获取列表底部总条数文本，如 '共 13 条'"""
        try:
            return self.page.locator('.el-pagination__total, text=/共.*条/').first.text_content().strip()
        except Exception:
            return ""

    def get_list_column_texts(self, col_index: int) -> list[str]:
        """获取列表指定列的所有文本（col_index 从1开始）"""
        self.page.wait_for_timeout(500)
        cells = self.page.locator(f'.el-table__body .el-table__row td:nth-child({col_index})').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def get_list_headers(self) -> list[str]:
        """获取列表表头"""
        headers = self.page.locator('.el-table__header th .cell').all()
        return [h.text_content().strip() for h in headers if h.text_content()]

    def is_list_empty(self) -> bool:
        """检查列表是否为空"""
        empty = self.page.locator('.el-table__empty-text, text="暂无数据"')
        return empty.count() > 0 or self.get_list_row_count() == 0

    # ==============================================================
    # 搜索与筛选
    # ==============================================================

    SEL_AGENT_SELECT = '.el-form-item:has-text("品牌所属代理商") .el-select'
    SEL_APPLY_DATE_START = '.el-form-item:has-text("申请时间") input:first-of-type'
    SEL_APPLY_DATE_END = '.el-form-item:has-text("申请时间") input:last-of-type'
    SEL_CITY_FILTER = '.el-form-item:has-text("选择品牌上架城市") .el-select'

    def search_by_keyword(self, keyword: str):
        """在搜索框输入关键字并点击搜索"""
        self.page.locator(self.SEL_SEARCH_INPUT).fill(keyword)
        self.page.locator(self.SEL_SEARCH_BTN).click()
        self.page.wait_for_timeout(1500)

    def click_search(self):
        """点击搜索按钮"""
        self.page.locator(self.SEL_SEARCH_BTN).click()
        self.page.wait_for_timeout(1500)

    def click_reset(self):
        """点击重置按钮"""
        self.page.locator(self.SEL_RESET_BTN).click()
        self.page.wait_for_timeout(1500)

    def select_agent_filter(self, index: int = 0):
        """选择品牌所属代理商筛选"""
        self.page.locator(self.SEL_AGENT_SELECT).click()
        self.page.wait_for_timeout(500)
        options = self.page.locator('.el-select-dropdown:visible .el-select-dropdown__item')
        if options.count() > index:
            options.nth(index).click()
        self.page.wait_for_timeout(300)

    def select_city_filter(self, city_name: str = ""):
        """选择品牌上架城市筛选"""
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
        """设置申请时间范围"""
        start_input = self.page.locator(self.SEL_APPLY_DATE_START)
        start_input.click()
        start_input.fill(start)
        end_input = self.page.locator(self.SEL_APPLY_DATE_END)
        end_input.click()
        end_input.fill(end)
        end_input.press("Enter")
        self.page.wait_for_timeout(500)

    def click_tab(self, tab_text: str):
        """点击状态标签（全部/申请中/已授权/已驳回/重新审核）"""
        self.page.locator(f'.el-tabs__item:has-text("{tab_text}")').click()
        self.page.wait_for_timeout(1500)

    def get_tab_text(self, tab_text: str) -> str:
        """获取标签完整文本（含数量），如 '全部（13）'"""
        try:
            return self.page.locator(f'.el-tabs__item:has-text("{tab_text}")').text_content().strip()
        except Exception:
            return ""

    def get_search_input_value(self) -> str:
        """获取搜索框当前值"""
        return self.page.locator(self.SEL_SEARCH_INPUT).input_value()

    def click_next_page(self):
        """点击下一页"""
        self.page.locator('button:has-text("下一页"), .btn-next').click()
        self.page.wait_for_timeout(1500)

    def select_page_size(self, size: str = "20"):
        """切换每页显示条数"""
        self.page.locator('.el-pagination .el-select').click()
        self.page.wait_for_timeout(500)
        self.page.locator(f'.el-select-dropdown:visible .el-select-dropdown__item:has-text("{size}")').click()
        self.page.wait_for_timeout(1500)

    # ==============================================================
    # 查看页面
    # ==============================================================

    def is_on_view_page(self) -> bool:
        """判断当前是否在品牌查看页"""
        return "isEdit=0" in self.current_url

    def is_on_edit_page(self) -> bool:
        """判断当前是否在品牌编辑页"""
        return "/coach/manage/edit" in self.current_url and "isEdit=0" not in self.current_url

    def get_view_title(self) -> str:
        """获取查看/编辑页面的标题文本"""
        page_content = self.page.content()
        if "查看品牌" in page_content:
            return "查看品牌"
        if "新增品牌" in page_content:
            return "新增品牌"
        if "编辑品牌" in page_content:
            return "编辑品牌"
        return ""

    def get_view_field(self, label: str) -> str:
        """获取查看页面某个字段的值（label : value 结构）"""
        try:
            # 查看页的字段结构：label ： value
            item = self.page.locator(f'text="{label}"').first
            parent = item.locator('..')
            return parent.text_content().replace(label, "").replace("：", "").replace(":", "").strip()
        except Exception:
            return ""

    def get_view_header_name(self) -> str:
        """获取查看页面顶部品牌名称"""
        try:
            # 查看页顶部信息区域的品牌名称（紧跟在头像后面的文字）
            content = self.page.content()
            # 在DOM中品牌名称以大字显示
            name_el = self.page.locator('.coach-detail-header .name, .detail-header .name').first
            if name_el.count() > 0:
                return name_el.text_content().strip()
        except Exception:
            pass
        return ""

    def get_view_stat_value(self, label: str) -> str:
        """获取查看页面统计数据的值"""
        try:
            stat = self.page.locator(f'text="{label}"').first
            parent = stat.locator('..')
            # 统计值在同一行的下方
            return parent.text_content().replace(label, "").strip()
        except Exception:
            return ""

    def view_page_has_text(self, text: str) -> bool:
        """检查查看页面是否包含指定文本"""
        return self.page.locator(f'text="{text}"').count() > 0

    def click_view_tab(self, tab_name: str):
        """在查看页面点击标签页（基础信息/服务记录/已关联规格/余额修改记录）"""
        self.page.locator(f'.el-tabs__item:has-text("{tab_name}")').click()
        self.page.wait_for_timeout(1000)

    def is_tab_active(self, tab_name: str) -> bool:
        """检查标签页是否处于选中状态"""
        tab = self.page.locator(f'.el-tabs__item:has-text("{tab_name}")')
        if tab.count() == 0:
            return False
        return "is-active" in (tab.get_attribute("class") or "")

    def click_modify_agent_btn(self):
        """点击修改经纪人按钮"""
        self.page.locator('button:has-text("修改经纪人")').click()
        self.page.wait_for_timeout(1000)

    def click_edit_account_btn(self):
        """点击新增编辑账号密码按钮"""
        self.page.locator('button:has-text("新增编辑账号密码")').click()
        self.page.wait_for_timeout(1000)

    def has_dialog_visible(self) -> bool:
        """检查是否有弹窗打开"""
        return self.page.locator('.el-dialog:visible, .el-dialog__wrapper:visible').count() > 0

    def close_dialog(self):
        """关闭弹窗"""
        try:
            close_btn = self.page.locator('.el-dialog:visible .el-dialog__headerbtn')
            if close_btn.count() > 0:
                close_btn.first.click()
                self.page.wait_for_timeout(500)
        except Exception:
            pass

    def click_view_return_btn(self):
        """点击查看页面的返回按钮"""
        self.page.locator('button:has-text("返回")').click()
        self.page.wait_for_timeout(1000)

    # ==============================================================
    # 编辑页面辅助方法
    # ==============================================================

    def goto_edit_brand(self, brand_name: str):
        """导航到品牌列表页，然后点击指定品牌的编辑按钮"""
        self.goto_brand_list()
        self._dismiss_notification()
        self.click_edit_by_name(brand_name)
        self.page.wait_for_selector(self.SEL_BRAND_NAME, state="visible", timeout=10000)

    def goto_view_brand(self, brand_name: str):
        """导航到品牌列表页，然后点击指定品牌的查看按钮"""
        self.goto_brand_list()
        self._dismiss_notification()
        self.click_view_by_name(brand_name)
        self.page.wait_for_timeout(2000)

    def clear_and_fill_brand_name(self, value: str):
        """清空并重新填写品牌名称"""
        self.page.locator(self.SEL_BRAND_NAME).fill("")
        self.page.locator(self.SEL_BRAND_NAME).fill(value)

    def clear_and_fill_brand_contact(self, value: str):
        """清空并重新填写品牌联系人"""
        self.page.locator(self.SEL_BRAND_CONTACT).fill("")
        self.page.locator(self.SEL_BRAND_CONTACT).fill(value)

    def clear_and_fill_commission_rate(self, value: str):
        """清空并重新填写提成比例"""
        self.page.locator(self.SEL_COMMISSION_RATE).fill("")
        self.page.locator(self.SEL_COMMISSION_RATE).fill(value)

    def clear_and_fill_brand_desc(self, value: str):
        """清空并重新填写品牌简介"""
        self.page.locator(self.SEL_BRAND_DESC).fill("")
        self.page.locator(self.SEL_BRAND_DESC).fill(value)

    def clear_and_fill_virtual_orders(self, value: str):
        """清空并重新填写虚拟订单量"""
        self.page.locator(self.SEL_VIRTUAL_ORDERS).fill("")
        self.page.locator(self.SEL_VIRTUAL_ORDERS).fill(value)
