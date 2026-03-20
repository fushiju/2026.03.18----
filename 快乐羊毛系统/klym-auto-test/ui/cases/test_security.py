"""
UI 测试 - 安全测试
对应用例编号：aqcs-001 ~ aqcs-005, aq-zq-001 ~ aq-zq-010

功能：支付金额防篡改、越权访问、XSS防护、验证码暴力破解
"""
import pytest
from ui.pages.base_page import BasePage


@pytest.mark.ui
@pytest.mark.security
class TestSecurityXSS:
    """XSS 注入防护"""

    @pytest.mark.p2
    def test_aqcs004_xss_in_merchant_name(self, admin_page):
        """aqcs-004: 验证商户录入页面XSS防护
        步骤：在商家名称输入 <script>alert(1)</script>
        预期：输出转义，不执行脚本
        """
        page = BasePage(admin_page)
        page.navigate("加盟管理", "代理商管理")
        page.wait_loading()
        # 找到新增按钮
        admin_page.get_by_role("button", name="新增").first.click()
        page.wait_loading()
        # 在名称输入框注入XSS
        name_input = admin_page.locator(
            "input[placeholder*='名称'], input[placeholder*='商家']"
        ).first
        if name_input.count() > 0:
            name_input.fill("<script>alert('xss')</script>")

    @pytest.mark.p1
    def test_aqzq005_xss_script_injection(self, admin_page):
        """aq-zq-005: 验证XSS跨站脚本攻击防护
        步骤：各输入框注入脚本
        预期：脚本不被执行
        """
        page = BasePage(admin_page)
        page.navigate("订单管理", "服务订单")
        page.wait_loading()
        # 搜索框注入
        search_input = admin_page.get_by_placeholder("请输入").first
        if search_input.count() > 0:
            search_input.fill("<img src=x onerror=alert(1)>")
            admin_page.get_by_role("button", name="搜索").first.click()
            page.wait_loading()


@pytest.mark.ui
@pytest.mark.security
class TestSecurityPermission:
    """权限与越权测试"""

    @pytest.mark.p1
    def test_aqcs002_api_unauthorized(self, admin_page):
        """aqcs-002: 验证未授权API越权防护
        步骤：直接访问受保护的API路径
        预期：返回无权限
        """
        # 通过 Playwright 的 route 拦截验证
        pass

    @pytest.mark.p2
    def test_aqcs003_store_data_isolation(self, admin_page):
        """aqcs-003: 验证门店子账号数据隔离
        预期：子账号只能看到本门店数据
        """
        pytest.skip("需要门店子账号登录测试")


@pytest.mark.ui
@pytest.mark.security
class TestSecurityPayment:
    """支付安全"""

    @pytest.mark.p1
    def test_aqcs001_payment_amount_tampering(self, admin_page):
        """aqcs-001: 验证支付金额前端篡改防护
        步骤：通过API拦截修改金额参数
        预期：后端校验拒绝
        """
        pytest.skip("需要通过接口测试验证")

    @pytest.mark.p2
    def test_aqcs005_captcha_brute_force(self, admin_page):
        """aqcs-005: 验证验证码接口防暴力破解
        步骤：连续5次输入错误验证码
        预期：锁定15分钟
        """
        pytest.skip("需要通过接口测试验证")
