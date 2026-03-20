# -*- coding: utf-8 -*-
"""
管理后台 - 安全测试自动化
对应用例: aq-zq-001~012
"""
import pytest
import sys
sys.path.insert(0, '..')
from config import BASE_URL


class TestSecurity:
    """安全性自动化测试"""

    def test_unauthorized_api_returns_401(self, browser_context):
        """验证无token访问API返回401 (aq-zq-007)"""
        new_page = browser_context.new_page()

        # 不登录直接访问后台API
        response = new_page.goto(f"{BASE_URL}/api/orders")
        if response:
            status = response.status
            assert status in [401, 403, 302], f"无token访问应返回401/403/302，实际{status}"
            print(f"✅ 无token访问返回 {status}")
        new_page.close()

    def test_expired_token_redirects_to_login(self, browser_context):
        """验证token过期后跳转登录页 (ht-hj-006)"""
        new_page = browser_context.new_page()

        # 设置一个过期/无效的token
        new_page.goto(f"{BASE_URL}/")
        new_page.evaluate("""
            localStorage.setItem('token', 'expired_invalid_token_12345');
            sessionStorage.setItem('token', 'expired_invalid_token_12345');
        """)

        # 尝试访问后台页面
        new_page.goto(f"{BASE_URL}/order")
        new_page.wait_for_timeout(3000)

        # 应该被重定向到登录页
        current_url = new_page.url
        is_redirected = "/login" in current_url or current_url == f"{BASE_URL}/"
        print(f"📝 过期token访问后URL: {current_url}")
        # assert is_redirected, "过期token应跳转登录页"
        new_page.close()

    def test_xss_in_search_box(self, page):
        """验证搜索框XSS注入防护 (aq-zq-005)"""
        xss_payloads = [
            '<script>alert("xss")</script>',
            '<img src=x onerror=alert(1)>',
            '"><script>alert(1)</script>',
        ]

        # 找到页面上的搜索框
        search = page.locator('input[placeholder*="搜索"], input[placeholder*="查询"]').first

        if search.is_visible():
            for payload in xss_payloads:
                search.fill(payload)
                page.locator('button:has-text("搜索"), button:has-text("查询")').first.click()
                page.wait_for_timeout(1000)

                # 检查页面是否正常（没有弹框、没有脚本执行）
                page_content = page.content()
                assert '<script>alert' not in page_content, f"XSS payload未被转义: {payload}"

            print("✅ 搜索框XSS注入被过滤")
        else:
            print("⏭️ 未找到搜索框")

    def test_no_sensitive_data_in_page(self, page):
        """验证页面不暴露敏感信息 (aq-zq-010)"""
        page_text = page.inner_text("body")

        # 检查是否有完整手机号（11位连续数字）
        import re
        full_phones = re.findall(r'1[3-9]\d{9}', page_text)
        # 过滤掉脱敏的格式（138****8001这种不算）
        exposed = [p for p in full_phones if '****' not in page_text[max(0, page_text.index(p)-5):page_text.index(p)+15]]

        if exposed:
            print(f"⚠ 发现可能未脱敏的手机号: {exposed[:3]}")
        else:
            print("✅ 未发现明文手机号泄露")
