# -*- coding: utf-8 -*-
"""
29_用户端_外卖区-通用券(V3.0补充) · 自动化测试
来源文件: 29_用户端_外卖区-通用券(V3.0补充).xlsx
用例数量: 2 条

运行方法:
  cd admin-web
  pytest tests/generated/test_29_用户端_外卖区-通用券_V3_0补充.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_29_用户端_外卖区-通用券_V3_0补充.py -v              # 无头模式
  pytest tests/generated/test_29_用户端_外卖区-通用券_V3_0补充.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test外卖区通用券V30补充:
    """29_用户端_外卖区-通用券(V3.0补充) (2条)"""

    @case("tyj-bc-001", title="验证重试发货的幂等性(不重复发放卡密)", priority="P2")
    def test_tyj_bc_001(self, page):
        """[tyj-bc-001] 验证重试发货的幂等性(不重复发放卡密)  [P2]"""
        # ── 前置条件 ──
        #   订单FAIL状态,运营点击重试
        #
        # ── 测试步骤 ──
        #   1. 运营点击"重试发货"
    #   2. 重试成功
    #   3. 查看卡密发放记录
        #
        # ── 预期结果 ──
        #   1. 重试成功,订单变为COMPLETED
    #   2. 用户仅收到1组卡密
    #   3. 不会重复发放
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("tyj-bc-002", title="验证卡密即将过期的标红提示", priority="P3")
    def test_tyj_bc_002(self, page):
        """[tyj-bc-002] 验证卡密即将过期的标红提示  [P3]"""
        # ── 前置条件 ──
        #   卡密有效期距今还有3天
        #
        # ── 测试步骤 ──
        #   1. 进入订单详情页
    #   2. 查看有效期展示
        #
        # ── 预期结果 ──
        #   1. 有效期文字标红
    #   2. 附"即将过期"标签
        #
        # ── 备注: 待确认问题Q11:阈值多少天 ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
