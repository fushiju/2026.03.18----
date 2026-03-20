# -*- coding: utf-8 -*-
"""
32_商家端_商家端-数据统计(V3.0补充) · 自动化测试
来源文件: 32_商家端_商家端-数据统计(V3.0补充).xlsx
用例数量: 2 条

运行方法:
  cd admin-web
  pytest tests/generated/test_32_商家端_商家端-数据统计_V3_0补充.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_32_商家端_商家端-数据统计_V3_0补充.py -v              # 无头模式
  pytest tests/generated/test_32_商家端_商家端-数据统计_V3_0补充.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test商家端数据统计V30补充:
    """32_商家端_商家端-数据统计(V3.0补充) (2条)"""

    @case("sjsj-bc-001", title="验证退款订单对流水统计的影响", priority="P2")
    def test_sjsj_bc_001(self, page):
        """[sjsj-bc-001] 验证退款订单对流水统计的影响  [P2]"""
        # ── 前置条件 ──
        #   本月10笔订单共1000元,其中1笔200元已退款
        #
        # ── 测试步骤 ──
        #   1. 查看本月流水统计
    #   2. 核对金额
        #
        # ── 预期结果 ──
        #   1. 需确认退款是否从流水扣除
    #   2. 如扣除:800元
    #   3. 如不扣除:1000元标注退款200元
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("sjsj-bc-002", title="验证三端数据一致性(用户/商家/后台)", priority="P2")
    def test_sjsj_bc_002(self, page):
        """[sjsj-bc-002] 验证三端数据一致性(用户/商家/后台)  [P2]"""
        # ── 前置条件 ──
        #   一笔餐饮扫码订单已完成
        #
        # ── 测试步骤 ──
        #   1. 用户端查看订单
    #   2. 商家端查看
    #   3. 后台查看
    #   4. 对比三端数据
        #
        # ── 预期结果 ──
        #   1. 三端订单金额一致
    #   2. 三端状态一致
    #   3. 三端时间一致
    #   4. 分佣数据只在后台可见
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
