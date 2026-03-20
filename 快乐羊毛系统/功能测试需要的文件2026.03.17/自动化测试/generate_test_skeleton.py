# -*- coding: utf-8 -*-
"""
从Excel用例自动生成自动化测试脚本骨架
核心规则：一个功能模块 = 一个文件，所有相关用例合并进去

用法：python generate_test_skeleton.py
"""
import sys, os, re, openpyxl
from collections import OrderedDict
sys.stdout.reconfigure(encoding='utf-8')

EXCEL_PATH = '../最终版测试用例/快乐羊毛系统完整测试用例2026.03.17（付仕菊）-V3.0完善版v2.xlsx'
OUTPUT_DIR = 'admin-web/tests/generated'

# ================================================================
# 模块归并映射表：把Excel里各种模块名归并到同一个功能文件
# key = 归并后的功能名, value = Excel里所有相关的模块名关键词
# ================================================================
MODULE_MERGE = OrderedDict([
    # ---- 用户端 ----
    ('user_01_免费资料区',      ['免费资料']),
    ('user_02_外卖红包',        ['外卖区-红包', '外卖区红包', '红包']),
    ('user_03_外卖通用券',      ['外卖区-通用券', '外卖区通用券', '通用券']),
    ('user_04_餐饮折扣_品牌直跳', ['连锁品牌直跳', '品牌直跳', 'CPS模式']),
    ('user_05_餐饮折扣_系统直连', ['系统直连', '模式一']),
    ('user_06_餐饮折扣_人工辅助', ['人工辅助', '验证码', '模式二']),
    ('user_07_打车服务',        ['打车']),
    ('user_08_电影票务',        ['电影']),
    ('user_09_会员充值',        ['充值']),
    ('user_10_家电购物',        ['家电', '京东联盟']),
    ('user_11_购物返利',        ['购物返利']),
    ('user_12_个人中心',        ['个人中心']),
    ('user_13_加油充电',        ['加油', '充电']),
    ('user_14_消息通知',        ['消息通知']),
    # ---- 商家端 ----
    ('merchant_01_账号与入驻',   ['账号体系', '品牌账号']),
    ('merchant_02_门店运营',     ['门店运营']),
    ('merchant_03_收银台',      ['收银台']),
    ('merchant_04_数据统计',     ['数据统计']),
    # ---- 管理后台 ----
    ('admin_01_分佣系统',       ['分佣系统', '分佣规则', '分佣场景', '分佣']),
    ('admin_02_订单状态机',      ['订单状态机', '退款规则']),
    ('admin_03_选品仓库',       ['选品仓库']),
    ('admin_04_商品类型管理',    ['商品类型', 'type_id']),
    ('admin_05_Excel佣金导入',  ['Excel', 'excel']),
    ('admin_06_代理商管理',      ['代理商管理']),
    ('admin_07_提现结算',       ['提现', '结算']),
    ('admin_08_退款分佣冲抵',    ['退款分佣', '冲抵']),
    # ---- 跨端/专项 ----
    ('cross_01_三端数据一致性',  ['三端', '一致性']),
    ('cross_02_安全测试',       ['安全']),
    ('cross_03_并发测试',       ['并发']),
    ('cross_04_性能测试',       ['性能', '数据边界']),
    ('cross_05_兼容性测试',     ['兼容性']),
    ('cross_06_网络异常',       ['网络异常']),
    ('cross_07_用户操作异常',    ['用户操作异常']),
    ('cross_08_环境测试',       ['环境测试', '管理后台环境', '管理后台异常', '商家端环境', '商家端异常', 'PC浏览器']),
])


def match_module(端, module_name):
    """根据模块名匹配归并后的功能名"""
    m = module_name.replace('\n', ' ').strip()
    for func_name, keywords in MODULE_MERGE.items():
        for kw in keywords:
            if kw in m:
                return func_name
    # 没匹配到，用原模块名
    safe = re.sub(r'[^\w\u4e00-\u9fff]', '_', m)
    safe = re.sub(r'_+', '_', safe).strip('_')[:25]
    端_prefix = {'用户端': 'user', '商家端': 'merchant', '管理后台': 'admin'}.get(端, 'other')
    return f'{端_prefix}_99_{safe}'


def sanitize_id(case_id):
    return case_id.replace('-', '_').replace('.', '_')


def generate_function(c):
    """生成单条用例的函数代码"""
    fid = sanitize_id(c['id'])
    title = c['title'].replace('"', '\\"').replace('\n', ' ')
    pri = c['priority']
    pre = c['precond'].replace('\n', '\n    #   ')
    steps = c['steps'].replace('\n', '\n    #   ')
    exp = c['expected'].replace('\n', '\n    #   ')

    return f'''
    @case("{c['id']}", title="{title}", priority="{pri}")
    def test_{fid}(self, page):
        """[{c['id']}] {title}  [{pri}]"""
        # ── 前置条件 ──
        #   {pre}
        #
        # ── 测试步骤 ──
        #   {steps}
        #
        # ── 预期结果 ──
        #   {exp}

        # TODO: 填写自动化代码，填完删掉下面的skip
        pytest.skip("待实现")
'''


def main():
    print("=" * 60)
    print("  一个功能 = 一个文件，从Excel生成测试骨架")
    print("=" * 60)

    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb['快乐羊毛测试用例']

    # 读取所有用例
    all_cases = []
    current_端 = ''
    current_module = ''
    for r in range(2, ws.max_row + 1):
        d = ws.cell(row=r, column=1).value
        m = ws.cell(row=r, column=5).value
        cid = ws.cell(row=r, column=3).value
        if d: current_端 = d
        if m: current_module = m
        if not cid or not cid.strip():
            continue
        all_cases.append({
            'id': cid.strip(),
            'priority': (ws.cell(row=r, column=4).value or '').strip(),
            'title': (ws.cell(row=r, column=6).value or '').strip(),
            'precond': (ws.cell(row=r, column=7).value or '').strip(),
            'steps': (ws.cell(row=r, column=8).value or '').strip(),
            'expected': (ws.cell(row=r, column=9).value or '').strip(),
            '端': current_端,
            'module': current_module,
        })

    # 按功能归并
    func_cases = OrderedDict()
    for c in all_cases:
        func_name = match_module(c['端'], c['module'])
        if func_name not in func_cases:
            func_cases[func_name] = []
        func_cases[func_name].append(c)

    # 清空旧文件
    import shutil
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 生成文件
    total_cases = 0
    for func_name, cases in func_cases.items():
        filename = f"test_{func_name}.py"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # 类名
        parts = func_name.split('_', 2)
        class_suffix = parts[2] if len(parts) > 2 else func_name
        class_name = 'Test' + ''.join(w.capitalize() for w in class_suffix.split('_') if w)

        # 统计来源
        sources = set()
        for c in cases:
            m = c['module'].replace('\n', ' ')
            sources.add(m[:30])

        # 按优先级排序：P0在前
        pri_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4}
        cases.sort(key=lambda x: pri_order.get(x['priority'], 5))

        content = f'''# -*- coding: utf-8 -*-
"""
{func_name} · 自动化测试
共 {len(cases)} 条用例
来源模块: {', '.join(sorted(sources))}

运行方法:
  pytest {filepath} -v --headed     # 有界面
  pytest {filepath} -v              # 无头模式
  pytest {filepath} -k "test_fyxt"  # 只跑编号含fyxt的
"""
import pytest
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import os
from utils.case_mapping import case


class {class_name}:
    """{func_name} ({len(cases)}条用例)"""
'''
        for c in cases:
            content += generate_function(c)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        total_cases += len(cases)
        print(f"  📝 {filename:<45s} {len(cases):>3d}条")

    print(f"\n{'='*60}")
    print(f"  生成完成: {len(func_cases)} 个文件, {total_cases} 条用例")
    print(f"  输出目录: {OUTPUT_DIR}/")
    print(f"{'='*60}")
    print(f"\n下一步:")
    print(f"  1. 打开文件，在 TODO 处填写 Playwright/automator 操作代码")
    print(f"  2. 填完后删掉 pytest.skip('待实现')")
    print(f"  3. 运行: pytest {OUTPUT_DIR}/test_admin_01_分佣系统.py -v")
    print(f"  4. 查看覆盖率: python coverage_report.py")


if __name__ == '__main__':
    main()
