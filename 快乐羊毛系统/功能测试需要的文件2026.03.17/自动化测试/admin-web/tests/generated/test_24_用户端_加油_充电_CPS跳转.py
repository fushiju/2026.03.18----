# -*- coding: utf-8 -*-
"""
24_用户端_加油_充电(CPS跳转) · 自动化测试
来源文件: 24_用户端_加油_充电(CPS跳转).xlsx
用例数量: 3 条

运行方法:
  cd admin-web
  pytest tests/generated/test_24_用户端_加油_充电_CPS跳转.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_24_用户端_加油_充电_CPS跳转.py -v              # 无头模式
  pytest tests/generated/test_24_用户端_加油_充电_CPS跳转.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test加油_充电CPS跳转:
    """24_用户端_加油_充电(CPS跳转) (3条)"""

    @case("jycz-001", title="验证加油/充电入口展示及位置权限请求", priority="P1")
    def test_jycz_001(self, page):
        """[jycz-001] 验证加油/充电入口展示及位置权限请求  [P1]"""
        # ── 前置条件 ──
        #   用户已登录平台,手机GPS已开启
        #
        # ── 测试步骤 ──
        #   1. 进入"加油/充电"页面
    #   2. 观察位置权限弹窗
    #   3. 允许授权后查看页面
        #
        # ── 预期结果 ──
        #   1. 页面正常加载
    #   2. 首次进入弹出微信位置授权弹窗
    #   3. 授权后展示附近加油站/充电桩列表,按距离排序
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("jycz-002", title="验证加油站/充电桩列表跳转第三方App", priority="P1")
    def test_jycz_002(self, page):
        """[jycz-002] 验证加油站/充电桩列表跳转第三方App  [P1]"""
        # ── 前置条件 ──
        #   用户已授权位置,列表展示至少3个站点
        #
        # ── 测试步骤 ──
        #   1. 查看列表展示信息
    #   2. 点击某加油站
    #   3. 确认跳转目标
        #
        # ── 预期结果 ──
        #   1. 列表展示站点名称、距离等信息
    #   2. 跳转至第三方App/H5
    #   3. 跳转链接携带渠道标识参数(CPS佣金追踪)
        #
        # ── 备注: 需确认具体对接渠道 ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("jycz-005", title="验证附近无站点时的空状态展示", priority="P3")
    def test_jycz_005(self, page):
        """[jycz-005] 验证附近无站点时的空状态展示  [P3]"""
        # ── 前置条件 ──
        #   用户位于偏远地区,附近无加油站/充电桩数据
        #
        # ── 测试步骤 ──
        #   1. 进入加油/充电页面
    #   2. 查看列表展示
        #
        # ── 预期结果 ──
        #   1. 列表为空
    #   2. 展示空状态占位图+"附近暂无站点"提示
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
