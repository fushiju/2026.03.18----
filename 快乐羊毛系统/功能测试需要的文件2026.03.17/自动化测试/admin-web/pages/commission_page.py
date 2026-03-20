# -*- coding: utf-8 -*-
"""分佣配置页面 Page Object"""
from config import BASE_URL


class CommissionPage:
    def __init__(self, page):
        self.page = page
        # ====== 选择器（根据实际页面修改）======
        self.menu_commission = 'text=分佣, [href*="commission"], .menu-item:has-text("分佣")'
        self.platform_rate = 'input[placeholder*="平台"], input[name*="platform"]'
        self.agent_rate = 'input[placeholder*="代理商"], input[name*="agent"]'
        self.distributor_l1 = 'input[placeholder*="一级"], input[name*="level1"]'
        self.distributor_l2 = 'input[placeholder*="二级"], input[name*="level2"]'
        self.save_btn = 'button:has-text("保存"), button:has-text("确定")'
        self.success_msg = '.el-message--success, .ant-message-success, [class*="success"]'
        self.error_msg = '.el-message--error, .ant-message-error, [class*="error"]'

    def goto(self):
        try:
            self.page.locator(self.menu_commission).first.click()
            self.page.wait_for_load_state("networkidle")
        except Exception:
            self.page.goto(f"{BASE_URL}/commission")
            self.page.wait_for_load_state("networkidle")
        return self

    def set_rates(self, platform=None, agent=None, level1=None, level2=None):
        """设置分佣比例"""
        if platform is not None:
            inp = self.page.locator(self.platform_rate).first
            inp.clear()
            inp.fill(str(platform))
        if agent is not None:
            inp = self.page.locator(self.agent_rate).first
            inp.clear()
            inp.fill(str(agent))
        if level1 is not None:
            inp = self.page.locator(self.distributor_l1).first
            inp.clear()
            inp.fill(str(level1))
        if level2 is not None:
            inp = self.page.locator(self.distributor_l2).first
            inp.clear()
            inp.fill(str(level2))
        return self

    def save(self):
        self.page.locator(self.save_btn).first.click()
        self.page.wait_for_timeout(1000)
        return self

    def has_success_msg(self):
        try:
            return self.page.locator(self.success_msg).first.is_visible(timeout=3000)
        except Exception:
            return False

    def has_error_msg(self):
        try:
            return self.page.locator(self.error_msg).first.is_visible(timeout=3000)
        except Exception:
            return False

    def get_error_text(self):
        try:
            return self.page.locator(self.error_msg).first.inner_text(timeout=3000)
        except Exception:
            return ""
