# -*- coding: utf-8 -*-
"""
从Excel用例自动生成自动化测试脚本骨架

用法：
  python generate_test_skeleton.py

效果：
  读取570条用例 → 按模块分组 → 每个模块生成一个.py测试文件
  每条用例 → 一个test_函数（带@case装饰器+注释+TODO）
  你只需要往函数里填操作代码
"""
import sys
import os
import re
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

EXCEL_PATH = '../最终版测试用例/快乐羊毛系统完整测试用例2026.03.17（付仕菊）-V3.0完善版v2.xlsx'
OUTPUT_DIR = 'admin-web/tests/generated'


def sanitize_id(case_id):
    """mfzl-001 → mfzl_001"""
    return case_id.replace('-', '_').replace('.', '_')


def sanitize_module(module_name):
    """模块名 → 文件名"""
    # 去除换行和特殊字符
    name = module_name.replace('\n', '_').replace(' ', '_')
    name = re.sub(r'[（(].*?[）)]', '', name)  # 去括号内容
    name = re.sub(r'[^\w\u4e00-\u9fff]', '_', name)  # 只保留字母数字中文
    name = re.sub(r'_+', '_', name).strip('_')
    return name[:30]  # 限制长度


def generate_test_function(case):
    """生成单条用例的测试函数代码"""
    func_name = f"test_{sanitize_id(case['id'])}"
    case_ids_str = f'"{case["id"]}"'
    title = case['title'].replace('"', '\\"').replace('\n', ' ')
    priority = case['priority']
    precond = case['precond'].replace('\n', '\n    #   ')
    steps = case['steps'].replace('\n', '\n    #   ')
    expected = case['expected'].replace('\n', '\n    #   ')

    code = f'''
    @case({case_ids_str}, title="{title}", priority="{priority}")
    def {func_name}(self, page):
        """
        [{case['id']}] {title}
        优先级: {priority}
        """
        # 前置条件:
        #   {precond}
        #
        # 测试步骤:
        #   {steps}
        #
        # 预期结果:
        #   {expected}

        # TODO: 在此编写自动化操作代码
        # 示例:
        # page.goto("https://red.jinyedaojia.com/xxx")
        # page.locator("选择器").click()
        # assert page.locator("选择器").is_visible()
        pytest.skip("待实现")
'''
    return code


def main():
    print("=" * 60)
    print("  从Excel用例生成自动化测试脚本骨架")
    print("=" * 60)

    # 读取Excel
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb['快乐羊毛测试用例']

    # 按模块+端分组
    cases_by_module = {}
    current_端 = ''
    current_module = ''

    for row_idx in range(2, ws.max_row + 1):
        端 = ws.cell(row=row_idx, column=1).value
        module = ws.cell(row=row_idx, column=5).value
        cid = ws.cell(row=row_idx, column=3).value
        priority = ws.cell(row=row_idx, column=4).value
        title = ws.cell(row=row_idx, column=6).value
        precond = ws.cell(row=row_idx, column=7).value
        steps = ws.cell(row=row_idx, column=8).value
        expected = ws.cell(row=row_idx, column=9).value

        if 端: current_端 = 端
        if module: current_module = module
        if not cid or not cid.strip():
            continue

        key = f"{current_端}|{current_module}"
        if key not in cases_by_module:
            cases_by_module[key] = []

        cases_by_module[key].append({
            'id': cid.strip(),
            'priority': (priority or '').strip(),
            'title': (title or '').strip(),
            'precond': (precond or '').strip(),
            'steps': (steps or '').strip(),
            'expected': (expected or '').strip(),
            '端': current_端,
            'module': current_module.replace('\n', ' '),
        })

    # 生成文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_count = 0
    case_count = 0

    for key, cases in cases_by_module.items():
        端, module = key.split('|', 1)
        safe_module = sanitize_module(module)
        端_prefix = {'用户端': 'user', '商家端': 'merchant', '管理后台': 'admin'}.get(端, 'other')

        filename = f"test_{端_prefix}_{safe_module}.py"
        filepath = os.path.join(OUTPUT_DIR, filename)

        class_name = f"Test{''.join(w.capitalize() for w in safe_module.split('_') if w)}"

        # 生成文件内容
        content = f'''# -*- coding: utf-8 -*-
"""
{端} - {module} 自动化测试
自动生成自 Excel 用例，共 {len(cases)} 条
生成命令: python generate_test_skeleton.py

使用方法：
  1. 在每个 test_ 函数的 TODO 处填写自动化操作代码
  2. 填完后删除 pytest.skip("待实现")
  3. 运行: pytest {filepath} -v --headed
"""
import pytest
import sys
sys.path.insert(0, '..')
from utils.case_mapping import case


class {class_name}:
    """{端} - {module} ({len(cases)}条用例)"""
'''
        for c in cases:
            content += generate_test_function(c)

        # 写文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        file_count += 1
        case_count += len(cases)
        print(f"  📝 {filename} ({len(cases)}条)")

    print(f"\n生成完成: {file_count}个文件, {case_count}条用例")
    print(f"输出目录: {OUTPUT_DIR}/")
    print(f"\n下一步: 打开生成的文件，在TODO处填写操作代码")


if __name__ == '__main__':
    main()
