# -*- coding: utf-8 -*-
"""
自动化覆盖率追踪报告

用法:
  python coverage_report.py

功能:
  1. 扫描所有测试脚本，提取 @case("xxx") 中的用例编号
  2. 对比Excel用例表，计算覆盖率
  3. 输出：哪些已自动化、哪些未自动化、覆盖率百分比
"""
import sys
import os
import re
import openpyxl
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

EXCEL_PATH = '../最终版测试用例/快乐羊毛系统完整测试用例2026.03.17（付仕菊）-V3.0完善版v2.xlsx'
SCAN_DIRS = ['admin-web/tests', 'admin-web/tests/generated', 'miniprogram/tests']


def scan_automated_cases(scan_dirs):
    """扫描所有测试文件，提取已自动化的用例编号"""
    automated = {}  # {case_id: {file, func, has_skip}}

    for scan_dir in scan_dirs:
        if not os.path.exists(scan_dir):
            continue
        for fname in os.listdir(scan_dir):
            if not fname.endswith(('.py', '.js', '.test.js')):
                continue
            filepath = os.path.join(scan_dir, fname)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 匹配 Python: @case("mfzl-001", "mfzl-002", ...)
            for match in re.finditer(r'@case\(([^)]+)\)', content):
                ids_str = match.group(1)
                case_ids = re.findall(r'"([^"]+)"', ids_str)
                # 找到对应的函数名
                func_match = re.search(r'def\s+(test_\w+)', content[match.end():match.end()+200])
                func_name = func_match.group(1) if func_match else '?'
                # 检查是否有 pytest.skip（表示待实现）
                skip_check = content[match.end():match.end()+500]
                has_skip = 'pytest.skip' in skip_check

                for cid in case_ids:
                    automated[cid] = {
                        'file': fname,
                        'func': func_name,
                        'implemented': not has_skip,
                    }

            # 匹配 JS: test('mfzl-001: ...', async () => {
            for match in re.finditer(r"test\(\s*'([^']+)'", content):
                test_title = match.group(1)
                cid_match = re.match(r'([\w-]+):', test_title)
                if cid_match:
                    cid = cid_match.group(1)
                    automated[cid] = {
                        'file': fname,
                        'func': test_title[:50],
                        'implemented': True,
                    }

    return automated


def read_excel_cases(excel_path):
    """读取Excel所有用例"""
    wb = openpyxl.load_workbook(excel_path)
    ws = wb['快乐羊毛测试用例']

    cases = []
    current_端 = ''
    current_module = ''
    for row_idx in range(2, ws.max_row + 1):
        端 = ws.cell(row=row_idx, column=1).value
        module = ws.cell(row=row_idx, column=5).value
        cid = ws.cell(row=row_idx, column=3).value
        priority = ws.cell(row=row_idx, column=4).value
        title = ws.cell(row=row_idx, column=6).value
        if 端: current_端 = 端
        if module: current_module = module
        if cid and cid.strip():
            cases.append({
                'id': cid.strip(),
                'priority': (priority or '').strip(),
                'title': (title or '').strip(),
                '端': current_端,
                'module': current_module.replace('\n', ' '),
            })
    return cases


def main():
    print('=' * 70)
    print('  快乐羊毛 · 自动化用例覆盖率报告')
    print('=' * 70)

    # 读取
    all_cases = read_excel_cases(EXCEL_PATH)
    automated = scan_automated_cases(SCAN_DIRS)

    total = len(all_cases)
    auto_count = 0
    impl_count = 0
    skeleton_count = 0

    # 按模块统计
    module_stats = defaultdict(lambda: {'total': 0, 'auto': 0, 'impl': 0})

    for c in all_cases:
        key = f"{c['端']}|{c['module'][:25]}"
        module_stats[key]['total'] += 1

        if c['id'] in automated:
            auto_count += 1
            module_stats[key]['auto'] += 1
            if automated[c['id']]['implemented']:
                impl_count += 1
                module_stats[key]['impl'] += 1
            else:
                skeleton_count += 1

    not_auto = total - auto_count

    # 输出总览
    print(f'\n  Excel总用例: {total}条')
    print(f'  已生成骨架: {auto_count}条 ({auto_count*100//total}%)')
    print(f'  已填写代码: {impl_count}条 ({impl_count*100//total}%)')
    print(f'  待填写代码: {skeleton_count}条')
    print(f'  未生成骨架: {not_auto}条')

    # 按模块输出
    print(f'\n{"模块":<35s} {"总数":>4s} {"已覆盖":>6s} {"已实现":>6s} {"覆盖率":>6s}')
    print('-' * 65)
    for key in sorted(module_stats.keys()):
        s = module_stats[key]
        rate = f"{s['auto']*100//s['total']}%" if s['total'] > 0 else '0%'
        print(f"  {key:<33s} {s['total']:>4d}   {s['auto']:>4d}    {s['impl']:>4d}   {rate:>5s}")

    # 未自动化的P0用例
    print(f'\n--- 未自动化的P0用例（优先补充）---')
    p0_not_auto = [c for c in all_cases if c['priority'] == 'P0' and c['id'] not in automated]
    if p0_not_auto:
        for c in p0_not_auto:
            print(f"  [{c['id']}] {c['title'][:50]}")
    else:
        print("  ✅ 所有P0用例均已覆盖")

    # 未自动化的P1用例（前20条）
    print(f'\n--- 未自动化的P1用例（前20条）---')
    p1_not_auto = [c for c in all_cases if c['priority'] == 'P1' and c['id'] not in automated]
    for c in p1_not_auto[:20]:
        print(f"  [{c['id']}] {c['title'][:50]}")
    if len(p1_not_auto) > 20:
        print(f"  ... 还有{len(p1_not_auto)-20}条")

    print('\n' + '=' * 70)


if __name__ == '__main__':
    main()
