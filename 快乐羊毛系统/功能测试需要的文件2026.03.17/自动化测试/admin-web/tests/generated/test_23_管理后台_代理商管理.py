# -*- coding: utf-8 -*-
"""
23_管理后台_代理商管理 · 自动化测试
来源文件: 23_管理后台_代理商管理.xlsx
用例数量: 3 条

运行方法:
  cd admin-web
  pytest tests/generated/test_23_管理后台_代理商管理.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_23_管理后台_代理商管理.py -v              # 无头模式
  pytest tests/generated/test_23_管理后台_代理商管理.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test代理商管理:
    """23_管理后台_代理商管理 (3条)"""

    @case("dlsg-001", title="验证代理商查看自己的分佣明细", priority="P1")
    def test_dlsg_001(self, page):
        """[dlsg-001] 验证代理商查看自己的分佣明细  [P1]"""
        # ── 前置条件 ──
        #   代理商已登录，有多笔已结算佣金
        #
        # ── 测试步骤 ──
        #   1. 进入代理商后台
    #   2. 查看佣金明细列表
        #
        # ── 预期结果 ──
        #   1. 展示每笔订单的佣金金额/订单号/时间
    #   2. 待结算和已结算分别展示
    #   3. 总金额汇总正确
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("dlsg-002", title="验证代理商查看下级分销员列表", priority="P1")
    def test_dlsg_002(self, page):
        """[dlsg-002] 验证代理商查看下级分销员列表  [P1]"""
        # ── 前置条件 ──
        #   代理商下有5个分销员
        #
        # ── 测试步骤 ──
        #   1. 进入代理商后台"分销管理"
    #   2. 查看分销员列表
        #
        # ── 预期结果 ──
        #   1. 展示5个分销员信息
    #   2. 每个分销员的推广订单数/佣金金额
    #   3. 支持按时间筛选
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("dlsg-003", title="验证代理商提现流程", priority="P2")
    def test_dlsg_003(self, page):
        """[dlsg-003] 验证代理商提现流程  [P2]"""
        # ── 前置条件 ──
        #   代理商可提现余额500元
        #
        # ── 测试步骤 ──
        #   1. 代理商申请提现300元
    #   2. 运营审核通过
    #   3. 查看到账
        #
        # ── 预期结果 ──
        #   1. 提现申请提交成功
    #   2. 运营审核通过
    #   3. 300元到账
    #   4. 余额变为200元
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
