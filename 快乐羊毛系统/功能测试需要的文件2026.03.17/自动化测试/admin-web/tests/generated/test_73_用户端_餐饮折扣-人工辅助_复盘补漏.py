# -*- coding: utf-8 -*-
"""
73_用户端_餐饮折扣-人工辅助(复盘补漏) · 自动化测试
来源文件: 73_用户端_餐饮折扣-人工辅助(复盘补漏).xlsx
用例数量: 1 条

运行方法:
  cd admin-web
  pytest tests/generated/test_73_用户端_餐饮折扣-人工辅助_复盘补漏.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_73_用户端_餐饮折扣-人工辅助_复盘补漏.py -v              # 无头模式
  pytest tests/generated/test_73_用户端_餐饮折扣-人工辅助_复盘补漏.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test餐饮折扣人工辅助复盘补漏:
    """73_用户端_餐饮折扣-人工辅助(复盘补漏) (1条)"""

    @case("cyzkrg-bl-001", title="验证同名商家是否允许重复录入", priority="P2")
    def test_cyzkrg_bl_001(self, page):
        """[cyzkrg-bl-001] 验证同名商家是否允许重复录入  [P2]"""
        # ── 前置条件 ──
        #   1. 已录入一个商家"张三烤肉店"
        #
        # ── 测试步骤 ──
        #   1. 再次录入一个同名商家"张三烤肉店"（不同地址）。
    #   2. 提交审核。
    #   3. 检查结果
        #
        # ── 预期结果 ──
        #   1. 允许录入（不同门店可能同名）并提交成功。
    #   2. 或系统提示"已存在同名商家，是否继续？"。
    #   3. 列表中两个同名商家可通过地址区分
        #
        # ── 备注: 需求2.3.3测试关注点：同名商家重复录入 ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
