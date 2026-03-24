"""品牌表单页 Page Object（新增 & 编辑共用）

对应页面：#/coach/manage/edit?isEdit=1
新增品牌和编辑品牌共用同一个表单，所以放在一个类里。
  - test_brand_add.py  使用本类
  - test_brand_edit.py 使用本类
"""
from pages.base_page import BasePage


class BrandFormPage(BasePage):

    # ---- 通过 placeholder 定位的表单字段（最可靠） ----
    SEL_BRAND_NAME = 'input[placeholder="请输入品牌名称"]'
    SEL_BRAND_CONTACT = 'input[placeholder="请输入品牌联系人手机号"]'
    SEL_COMMISSION_RATE = 'input[placeholder="请输入提成比例"]'
    SEL_BRAND_DESC = 'textarea[placeholder="请输入品牌简介"]'
    SEL_VIRTUAL_ORDERS = 'input[placeholder="请输入虚拟订单量"]'
    SEL_SUBMIT_BTN = 'button:has-text("提交")'
    SEL_BACK_BTN = 'button:has-text("返回")'

    # ---- 反馈提示 ----
    SEL_SUCCESS_MSG = '.el-message--success'
    SEL_ERROR_MSG = '.el-message--error, .el-message--warning'
    SEL_FORM_ERROR = '.el-form-item__error'

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
        try:
            self.page.locator('button:has-text("新增品牌")').click(timeout=5000)
        except Exception:
            # 可能有延迟弹出的通知遮挡了按钮，再次关闭后重试
            self._dismiss_notification()
            self.page.locator('button:has-text("新增品牌")').click(timeout=5000)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self._dismiss_notification()
        self.page.wait_for_selector(self.SEL_BRAND_NAME, state="visible", timeout=10000)

    def goto_edit_brand(self, brand_name: str):
        """从列表页点击指定品牌的"编辑"按钮进入编辑表单"""
        self.goto_brand_list()
        self._dismiss_notification()
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")').first
        try:
            row.locator('button:has-text("编辑")').click(timeout=5000)
        except Exception:
            self._dismiss_notification()
            row.locator('button:has-text("编辑")').click(timeout=5000)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self._dismiss_notification()
        self.page.wait_for_selector(self.SEL_BRAND_NAME, state="visible", timeout=10000)

    def _dismiss_notification(self):
        """关闭所有可能遮挡页面的弹窗（来单通知等），最多尝试5次"""
        try:
            for _ in range(5):
                btn = self.page.locator(
                    '.el-dialog:visible button:has-text("忽 略"), '
                    '.el-dialog:visible button:has-text("忽略"), '
                    '.el-dialog:visible button:has-text("关闭"), '
                    '.el-dialog:visible .el-dialog__headerbtn, '
                    '.el-message-box__btns button:has-text("确定")'
                )
                if btn.count() > 0:
                    btn.first.click()
                    self.page.wait_for_timeout(800)
                else:
                    break
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

    def _locate_form_item(self, label_text: str):
        """通过 label 文本定位表单项（避免 CSS :has(:has-text()) 不稳定）"""
        return self.page.locator(f'.el-form-item__label:text-is("{label_text}")').locator('..')

    def _select_dropdown_by_label(self, label_text: str, index: int = 0):
        """通过 label 文本找到下拉框并选择第 index 项"""
        # 1. 先点页面标题区域关闭残留弹层
        self.page.locator('.el-form-item__label').first.click()
        self.page.wait_for_timeout(500)

        # 2. 点击目标下拉框的 wrapper 展开选项
        form_item = self._locate_form_item(label_text)
        wrapper = form_item.locator('.el-select__wrapper')
        wrapper.click()
        self.page.wait_for_timeout(1000)

        # 3. 找到最后一个可见的下拉面板（因为 Element Plus 用 teleport，新展开的在最后）
        visible_options = self.page.locator('.el-select-dropdown__item:visible')
        count = visible_options.count()
        if count > index:
            visible_options.nth(index).click()
        self.page.wait_for_timeout(500)

    def select_city(self, index: int = 0):
        self._select_dropdown_by_label("品牌上架城市", index)

    def select_category_type(self, index: int = 0):
        self._select_dropdown_by_label("分类类型", index)

    def select_api_channel(self, index: int = 0):
        self._select_dropdown_by_label("接口渠道", index)

    def select_sold_out(self, sold_out: bool = True):
        label = "售罄" if sold_out else "未售罄"
        self.page.locator(f'.el-radio__label:text-is("{label}")').click()

    def upload_brand_icon(self, file_path: str = "", force_upload: bool = False):
        """上传品牌ICON（从图片选择弹窗中选择或上传）"""
        trigger = self._locate_form_item("品牌ICON").locator('.upload-container .img-wrap')
        self._pick_image_from_dialog_el(trigger, file_path, force_upload=force_upload)

    def upload_brand_image(self, file_path: str = "", force_upload: bool = False):
        """上传品牌图片（从图片选择弹窗中选择或上传）"""
        trigger = self._locate_form_item("品牌图片").locator('.upload-container .img-wrap')
        self._pick_image_from_dialog_el(trigger, file_path, force_upload=force_upload)

    def _pick_image_from_dialog_el(self, trigger_locator, file_path: str = "",
                                    force_upload: bool = False):
        """通用图片上传（接收 locator 对象）

        Args:
            force_upload: 为 True 时跳过已有图片，强制通过 file input 上传指定文件。
                          用于测试文件格式/大小校验等场景。
        """
        trigger_locator.click()
        upload_dialog = self.page.locator('.el-dialog:visible:has-text("图片上传"), .el-dialog:visible:has-text("图片选择")')
        upload_dialog.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(1500)

        # 尝试多种选择器匹配图片项
        img_items = upload_dialog.locator('.imgItem, .img-item, .image-item')
        if not force_upload and img_items.count() > 0:
            img_items.first.click()
            self.page.wait_for_timeout(500)
            # 双击确保选中（某些UI需要）
            if not self._is_item_selected(upload_dialog):
                img_items.first.click()
                self.page.wait_for_timeout(500)
        elif file_path:
            # 点击"上传"按钮或直接设置文件
            file_input = upload_dialog.locator('input[type="file"]')
            file_input.set_input_files(file_path)
            self.page.wait_for_timeout(3000)
            new_items = upload_dialog.locator('.imgItem, .img-item, .image-item')
            if new_items.count() > 0:
                new_items.first.click()
                self.page.wait_for_timeout(500)

        upload_dialog.locator('button:has-text("确定")').click()
        self.page.wait_for_timeout(1500)

    def _is_item_selected(self, dialog_locator) -> bool:
        """检查弹窗中是否已选中至少一项"""
        try:
            selected_text = dialog_locator.locator('text=/已选.*[1-9]/').count()
            return selected_text > 0
        except Exception:
            return False

    def upload_brand_video(self, file_path: str = ""):
        """上传品牌视频（从视频选择弹窗中选择或上传）"""
        self._locate_form_item("品牌视频").locator('button:has-text("选择")').click()
        self.page.wait_for_timeout(1500)
        video_dialog = self.page.locator(
            '.el-dialog:visible:has-text("视频上传"), '
            '.el-dialog:visible:has-text("视频选择"), '
            '.el-dialog:visible:has-text("视频")'
        )
        if video_dialog.count() == 0:
            return
        video_dialog.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(1500)

        # 优先选择已有的视频项（与图片上传弹窗逻辑相同）
        video_items = video_dialog.locator('.imgItem, .video-item, .file-item, .img-item')
        if video_items.count() > 0:
            video_items.first.click()
            self.page.wait_for_timeout(500)
        elif file_path:
            # 没有已有视频，尝试上传新文件
            file_input = video_dialog.locator('input[type="file"]')
            if file_input.count() > 0:
                file_input.set_input_files(file_path)
                self.page.wait_for_timeout(3000)
                new_items = video_dialog.locator('.imgItem, .video-item, .file-item, .img-item')
                if new_items.count() > 0:
                    new_items.first.click()
                    self.page.wait_for_timeout(500)

        confirm_btn = video_dialog.locator('button:has-text("确定")')
        if confirm_btn.count() > 0:
            confirm_btn.click()
            self.page.wait_for_timeout(1500)

    def set_commission_date(self, start_date: str, end_date: str):
        """设置提成限期日期（通过日期面板内的输入框设置）"""
        date_item = self._locate_form_item("提成限期日期")
        wrapper_inputs = date_item.locator('input.el-range-input')

        # 点击开始日期输入框，打开日期面板
        wrapper_inputs.first.click()
        self.page.wait_for_timeout(1000)

        # 在弹出的日期面板中填写日期
        picker_panel = self.page.locator('.el-picker-panel:visible')
        if picker_panel.count() > 0:
            # 找到面板内的"开始日期"和"结束日期"输入框
            start_input = picker_panel.locator('input[placeholder="开始日期"]')
            end_date_input = picker_panel.locator('input[placeholder="结束日期"]')

            if start_input.count() > 0:
                start_input.click()
                start_input.fill(start_date)
                start_input.press("Enter")
                self.page.wait_for_timeout(500)

            if end_date_input.count() > 0:
                end_date_input.click()
                end_date_input.fill(end_date)
                end_date_input.press("Enter")
                self.page.wait_for_timeout(500)

            # 点击确定按钮（如果有）
            confirm = picker_panel.locator('button:has-text("确定"), button:has-text("确认")')
            if confirm.count() > 0:
                confirm.click()
                self.page.wait_for_timeout(500)

        # 关闭残留的日期面板
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(300)

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
        # 先关闭可能残留的下拉弹层
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(300)
        self.page.locator(self.SEL_SUBMIT_BTN).scroll_into_view_if_needed()
        self.page.locator(self.SEL_SUBMIT_BTN).click()
        # 等待页面跳转（成功后会回到列表页）或消息弹窗
        for _ in range(16):
            self.page.wait_for_timeout(500)
            url = self.page.url
            if "/coach/manage" in url and "/edit" not in url:
                return  # 成功跳转到列表页
            if self.page.locator(self.SEL_SUCCESS_MSG).count() > 0:
                return  # 出现成功提示
            if self.page.locator(self.SEL_ERROR_MSG).count() > 0:
                return  # 出现错误提示
            if self.page.locator(self.SEL_FORM_ERROR).count() > 0:
                return  # 出现表单校验错误

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
        try:
            el = self._locate_form_item(field_label).locator('.el-form-item__error')
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

    def _get_form_item_text(self, label: str, inner_sel: str) -> str:
        try:
            locator = self._locate_form_item(label).locator(inner_sel)
            if locator.count() > 0:
                return locator.first.text_content().strip()
            return ""
        except Exception:
            return ""

    def get_brand_name_count(self) -> str:
        return self._get_form_item_text(
            "品牌名称",
            '.el-input__count-inner, .el-input__suffix-inner, .el-input__count'
        )

    def get_brand_contact_count(self) -> str:
        return self._get_form_item_text(
            "品牌联系人",
            '.el-input__count-inner, .el-input__suffix-inner, .el-input__count'
        )

    def get_brand_desc_count(self) -> str:
        return self._get_form_item_text(
            "品牌简介",
            '.el-input__count, .el-input__count-inner, .el-textarea__count-inner'
        )

    def is_submit_button_enabled(self) -> bool:
        return self.page.locator(self.SEL_SUBMIT_BTN).is_enabled()

    def has_icon_preview(self) -> bool:
        container = self._locate_form_item("品牌ICON").locator('.upload-container')
        # 检查 img 标签或 el-image 组件（即使图片加载失败也算已上传）
        return (container.locator('img').count() > 0
                or container.locator('.el-image').count() > 0)

    def has_image_preview(self) -> bool:
        container = self._locate_form_item("品牌图片").locator('.upload-container')
        return (container.locator('img').count() > 0
                or container.locator('.el-image').count() > 0)

    def brand_exists_in_list(self, brand_name: str) -> bool:
        self.page.wait_for_timeout(1000)
        return self.page.locator(f'text="{brand_name}"').count() > 0

    def get_list_brand_names(self) -> list[str]:
        self.page.wait_for_timeout(500)
        cells = self.page.locator('.el-table__body .el-table__row td:nth-child(3)').all()
        return [c.text_content().strip() for c in cells if c.text_content()]

    def click_edit_by_name(self, brand_name: str):
        row = self.page.locator(f'.el-table__row:has-text("{brand_name}")').first
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
