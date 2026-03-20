# -*- coding: utf-8 -*-
"""
用户端_登录 · 自动化测试
来源文件: 用户端_登录.xlsx
用例数量: 1 条

运行方法:
  cd admin-web
  pytest tests/generated/test_用户端_登录.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_用户端_登录.py -v              # 无头模式
  pytest tests/generated/test_用户端_登录.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test登录:
    """用户端_登录 (1条)"""

    @case("dl-001", title="", priority="P1")
    def test_dl_001(self, page):
        """[dl-001]   [P1]"""
        # ── 前置条件 ──
        #   无
        #
        # ── 测试步骤 ──
        #   无
        #
        # ── 预期结果 ──
        #   无
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
