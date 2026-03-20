# -*- coding: utf-8 -*-
"""
34_管理后台_安全性测试(V3.0补充) · 自动化测试
来源文件: 34_管理后台_安全性测试(V3.0补充).xlsx
用例数量: 4 条

运行方法:
  cd admin-web
  pytest tests/generated/test_34_管理后台_安全性测试_V3_0补充.py -v --headed     # 看浏览器操作
  pytest tests/generated/test_34_管理后台_安全性测试_V3_0补充.py -v              # 无头模式
  pytest tests/generated/test_34_管理后台_安全性测试_V3_0补充.py -k "test_xxx"   # 只跑某条
"""
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.case_mapping import case


class Test安全性测试V30补充:
    """34_管理后台_安全性测试(V3.0补充) (4条)"""

    @case("aqcs-bc-001", title="验证支付金额防篡改", priority="P1")
    def test_aqcs_bc_001(self, page):
        """[aqcs-bc-001] 验证支付金额防篡改  [P1]"""
        # ── 前置条件 ──
        #   用户下单购买10元通用券,售价9.5元
        #
        # ── 测试步骤 ──
        #   1. 使用抓包工具拦截支付请求
    #   2. 将金额从9.5改为0.01
    #   3. 放行请求
    #   4. 查看后端处理
        #
        # ── 预期结果 ──
        #   1. 后端校验金额不一致
    #   2. 拒绝该支付请求
    #   3. 订单状态不变
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("aqcs-bc-002", title="验证XSS防护", priority="P1")
    def test_aqcs_bc_002(self, page):
        """[aqcs-bc-002] 验证XSS防护  [P1]"""
        # ── 前置条件 ──
        #   用户在输入框中操作
        #
        # ── 测试步骤 ──
        #   1. 在消费金额输入框输入脚本代码
    #   2. 在商家名称字段输入恶意代码
    #   3. 提交后查看页面
        #
        # ── 预期结果 ──
        #   1. 输入被转义或拦截
    #   2. 页面不执行脚本
    #   3. 展示转义后的文本
        #
        # ── 备注: 覆盖所有用户输入字段 ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("aqcs-bc-003", title="验证API接口鉴权", priority="P2")
    def test_aqcs_bc_003(self, page):
        """[aqcs-bc-003] 验证API接口鉴权  [P2]"""
        # ── 前置条件 ──
        #   准备过期token和无效token
        #
        # ── 测试步骤 ──
        #   1. 使用过期token请求API
    #   2. 使用无效token请求
    #   3. 不携带token请求
        #
        # ── 预期结果 ──
        #   1. 三种情况均返回401
    #   2. 不返回业务数据
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")

    @case("aqcs-bc-004", title="验证越权操作防护(跨门店数据访问)", priority="P2")
    def test_aqcs_bc_004(self, page):
        """[aqcs-bc-004] 验证越权操作防护(跨门店数据访问)  [P2]"""
        # ── 前置条件 ──
        #   门店A子账号登录,已知门店B订单ID
        #
        # ── 测试步骤 ──
        #   1. 门店A请求门店B订单详情
    #   2. 修改API参数中的门店ID
        #
        # ── 预期结果 ──
        #   1. 返回"无权限"或"数据不存在"
    #   2. 不返回门店B的数据
        #
        # ── 备注:  ──

        # ↓↓↓ 在这里写自动化代码，写完删掉skip ↓↓↓
        pytest.skip("待实现")
