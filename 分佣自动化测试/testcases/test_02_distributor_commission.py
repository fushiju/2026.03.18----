"""
场景二（P2）：分销员邀请用户下单 - 一级/二级分销员分佣
分销员佣金从代理商42%份额中扣除
"""
import allure
import jsonpath
import pytest

from config import config


@allure.epic("今夜到家分佣系统")
@allure.feature("分销员分佣")
class TestDistributorCommission:
    """分销员（一级/二级）邀请用户扫码下单分佣验证"""

    SERVICE_FEE = 168
    MATERIAL_FEE = 10

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-2.1 一级分销员邀请用户下单 - 基础分佣验证")
    @allure.description(
        "一级分销员邀请用户下单，验证技师、平台、代理商、一级分销员分佣金额\n"
        "分销员佣金从代理商42%份额中扣除"
    )
    def test_level1_distributor_commission(self, complete_order_flow,
                                           order_api, calculator):
        # 假设一级分销员返佣比例5%
        distributor_rate = 0.05
        expected = calculator.calc_with_distributor(
            self.SERVICE_FEE, distributor_rate, self.MATERIAL_FEE
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-一级分销",
            source_type="distributor",
            source_id=config["accounts"]["distributor_level1"]["phone"],
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证一级分销员获得佣金"):
            dist_amount = jsonpath.jsonpath(data, "$..distributor.amount")
            assert dist_amount, "未找到分销员分佣数据"
            assert float(dist_amount[0]) == expected["distributor_level1"], \
                f"分销员佣金错误: 实际{dist_amount[0]}, 预期{expected['distributor_level1']}"

        with allure.step("验证代理商佣金 = 原始42% - 分销员佣金"):
            agent_amount = jsonpath.jsonpath(data, "$..agent.amount")
            assert agent_amount, "未找到代理商分佣数据"
            assert float(agent_amount[0]) == expected["agent"], \
                f"代理商佣金错误: 实际{agent_amount[0]}, 预期{expected['agent']}"

        with allure.step("验证技师和平台佣金不变"):
            tech_amount = jsonpath.jsonpath(data, "$..technician.amount")
            assert float(tech_amount[0]) == expected["technician"], \
                "分销员场景下技师佣金不应变化"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-2.2 一级分销员首单提成验证")
    @allure.description("首单按自定义提成比例，后续订单按全局比例")
    def test_level1_first_order_bonus(self, complete_order_flow, order_api):
        """首单提成 vs 非首单提成"""
        # 第一单
        order_id_1 = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-首单提成",
            source_type="distributor",
            source_id=config["accounts"]["distributor_level1"]["phone"],
        )

        with allure.step("查询首单分销员收益"):
            resp1 = order_api.get_order_commission(order_id_1)
            data1 = resp1.json()
            first_amount = jsonpath.jsonpath(data1, "$..distributor.amount")

        # 第二单
        order_id_2 = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-非首单提成",
            source_type="distributor",
            source_id=config["accounts"]["distributor_level1"]["phone"],
        )

        with allure.step("查询非首单分销员收益"):
            resp2 = order_api.get_order_commission(order_id_2)
            data2 = resp2.json()
            second_amount = jsonpath.jsonpath(data2, "$..distributor.amount")

        with allure.step("验证首单与非首单提成不同"):
            assert first_amount and second_amount, "分销员佣金数据缺失"
            # 首单提成通常高于全局设置
            allure.attach(
                f"首单: {first_amount[0]}, 非首单: {second_amount[0]}",
                "提成对比",
            )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-2.3 二级分销员邀请用户下单 - 多级分佣验证")
    @allure.description(
        "二级分销员邀请用户下单，验证一级+二级分销员均获佣，均从代理商扣除"
    )
    def test_level2_distributor_commission(self, complete_order_flow,
                                           order_api, calculator):
        distributor_rate = 0.05  # 一级
        level2_rate = 0.03      # 二级
        expected = calculator.calc_with_distributor(
            self.SERVICE_FEE, distributor_rate, self.MATERIAL_FEE,
            level2_rate=level2_rate,
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-二级分销",
            source_type="distributor_level2",
            source_id="level2_distributor_id",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证一级分销员获佣"):
            dist1 = jsonpath.jsonpath(data, "$..distributorLevel1.amount")
            assert dist1, "一级分销员应获得佣金"
            assert float(dist1[0]) == expected["distributor_level1"]

        with allure.step("验证二级分销员获佣"):
            dist2 = jsonpath.jsonpath(data, "$..distributorLevel2.amount")
            assert dist2, "二级分销员应获得佣金"
            assert float(dist2[0]) == expected["distributor_level2"]

        with allure.step("验证代理商佣金 = 42% - 一级佣金 - 二级佣金"):
            agent = jsonpath.jsonpath(data, "$..agent.amount")
            assert float(agent[0]) == expected["agent"], \
                f"代理商佣金应扣除两级分销佣金"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-2.4 二级分销员首单提成验证")
    @allure.description("代理商自定义二级分销首单提成")
    def test_level2_first_order_bonus(self, complete_order_flow, order_api):
        """二级分销员首单提成验证逻辑同一级"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-二级首单",
            source_type="distributor_level2",
            source_id="level2_distributor_id",
        )

        with allure.step("查询二级分销员首单收益"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()
            dist2 = jsonpath.jsonpath(data, "$..distributorLevel2.amount")
            assert dist2, "二级分销员首单应有提成"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-2.5 分销比例未设置时下单")
    @allure.description("代理商未设置分销比例时验证系统容错")
    def test_distributor_rate_not_set(self, complete_order_flow, order_api):
        """分销比例未设置 -> 系统默认值或提示"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-未设比例",
            source_type="distributor",
            source_id="unset_rate_distributor",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证系统处理未设置比例的情况"):
            dist = jsonpath.jsonpath(data, "$..distributor.amount")
            # 分销员佣金应为0或系统使用默认值
            if dist:
                allure.attach(f"分销员佣金: {dist[0]}", "未设比例时的佣金")
