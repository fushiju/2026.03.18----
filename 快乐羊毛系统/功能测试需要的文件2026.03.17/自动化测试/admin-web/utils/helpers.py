# -*- coding: utf-8 -*-
"""通用工具方法"""
import os
from config import SCREENSHOT_DIR


def take_screenshot(page, name):
    """手动截图"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path)
    print(f"  📸 截图: {path}")
    return path


def wait_for_table_loaded(page, timeout=10000):
    """等待后台表格加载完成（通用）"""
    # 常见的表格/列表选择器
    selectors = [
        "table tbody tr",
        ".el-table__body tr",
        ".ant-table-tbody tr",
        "[class*='table'] [class*='row']",
    ]
    for sel in selectors:
        try:
            page.wait_for_selector(sel, timeout=timeout)
            return True
        except Exception:
            continue
    return False


def get_table_row_count(page):
    """获取表格当前行数"""
    selectors = [
        "table tbody tr",
        ".el-table__body tr",
        ".ant-table-tbody tr",
    ]
    for sel in selectors:
        rows = page.locator(sel)
        if rows.count() > 0:
            return rows.count()
    return 0


def fill_and_submit_form(page, fields: dict, submit_text="保存"):
    """通用表单填写并提交
    fields: {'placeholder或label': 'value', ...}
    """
    for key, value in fields.items():
        input_el = page.locator(f'input[placeholder*="{key}"], label:has-text("{key}") + input').first
        input_el.fill(str(value))
    page.locator(f'button:has-text("{submit_text}")').first.click()
