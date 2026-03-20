# -*- coding: utf-8 -*-
"""
28_用户端_外卖区-红包(V3.0补充) · 自动化测试
来源文件: 28_用户端_外卖区-红包(V3.0补充).xlsx
用例数量: 2 条

运行方法:
  cd admin-web
  pytest tests/generated/test_28_用户端_外卖区-红包_V3_0补充.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_28_用户端_外卖区-红包_V3_0补充.py -v              # 无头模式
  pytest tests/generated/test_28_用户端_外卖区-红包_V3_0补充.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test外卖区红包V30补充:
    """28_用户端_外卖区-红包(V3.0补充) (2条)"""

    @case("wmhb-bc-001", title="验证多渠道佣金比例相同时的优选策略", priority="P2")
    def test_wmhb_bc_001(self, page):
        """[wmhb-bc-001] 验证多渠道佣金比例相同时的优选策略  [P2]"""
        # ── 前置条件 ──
        #   3个渠道佣金比例均为8%,优选模式开启
        #
        # ── 测试步骤 ──
        #   1. 点击美团红包Icon
    #   2. 查看后台日志确认使用的渠道
        #
        # ── 预期结果 ──
        #   1. 正常跳转成功
    #   2. 确认是否有默认优先级(如按配置顺序)
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("wmhb-bc-002", title="验证轮询模式下应用重启后计数器状态", priority="P2")
    def test_wmhb_bc_002(self, page):
        """[wmhb-bc-002] 验证轮询模式下应用重启后计数器状态  [P2]"""
        # ── 前置条件 ──
        #   轮询模式开启,已请求2次
        #
        # ── 测试步骤 ──
        #   1. 重启小程序/服务
    #   2. 再次点击美团红包Icon
    #   3. 查看后台日志
        #
        # ── 预期结果 ──
        #   1. 需确认:重启后计数器是否重置
    #   2. 如果持久化:第3次应请求凡点
    #   3. 如果重置:可能请求美赚
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
