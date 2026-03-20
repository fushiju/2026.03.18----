# -*- coding: utf-8 -*-
"""
管理后台 - 分佣配置自动化测试
对应用例: fyxt-001~026, fybc-001~012, fyxt-bl-001~002
"""
import pytest
import sys
sys.path.insert(0, '..')
from pages.commission_page import CommissionPage


class TestCommissionConfig:
    """分佣比例配置测试"""

    def test_set_normal_rates_50_50(self, page):
        """验证正常比例50%+50%保存成功 (fyxt-001)"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=50, agent=50).save()

        assert cp.has_success_msg(), "50%+50%应保存成功"
        print("✅ 平台50% + 代理商50% 保存成功")

    def test_set_normal_rates_30_70(self, page):
        """验证正常比例30%+70%保存成功 (fyxt-002)"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=30, agent=70).save()

        assert cp.has_success_msg(), "30%+70%应保存成功"
        print("✅ 平台30% + 代理商70% 保存成功")

    def test_rates_exceed_100_rejected(self, page):
        """验证比例合计>100%保存失败 (fybc-001)"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=60, agent=50).save()

        assert cp.has_error_msg(), "60%+50%=110%应保存失败"
        error = cp.get_error_text()
        print(f"✅ 超100%被拦截, 提示: {error}")

    def test_negative_rate_rejected(self, page):
        """验证负数比例被拦截"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=-5, agent=105).save()

        assert cp.has_error_msg(), "负数比例应被拦截"
        print("✅ 负数比例被拦截")

    def test_zero_rate_allowed(self, page):
        """验证0%比例允许（该角色不参与分佣）"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=0, agent=100).save()

        assert cp.has_success_msg(), "0%+100%应允许"
        print("✅ 平台0% + 代理商100% 保存成功")

    def test_distributor_exceeds_agent_rejected(self, page):
        """验证分销员比例超过代理商份额被拦截 (fybc-003)"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=50, agent=50, level1=30, level2=25).save()

        # 一级30% + 二级25% = 55% > 代理商50%
        assert cp.has_error_msg(), "分销员比例超过代理商应被拦截"
        print("✅ 分销员超出代理商被拦截")

    def test_distributor_equals_agent_allowed(self, page):
        """验证分销员比例=代理商份额允许"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=50, agent=50, level1=25, level2=25).save()

        # 25%+25%=50% = 代理商50%，代理商实得0
        assert cp.has_success_msg(), "分销员=代理商应允许（代理商实得0）"
        print("✅ 分销员=代理商允许")

    def test_decimal_rate(self, page):
        """验证小数比例如8.5%是否允许 (待确认Q18)"""
        cp = CommissionPage(page).goto()
        cp.set_rates(platform=50.5, agent=49.5).save()

        # 不管允许还是拒绝，记录结果
        if cp.has_success_msg():
            print("📝 小数比例(50.5%+49.5%)被允许")
        elif cp.has_error_msg():
            print(f"📝 小数比例被拒绝: {cp.get_error_text()}")
        else:
            print("📝 小数比例操作结果不明确，需人工确认")
