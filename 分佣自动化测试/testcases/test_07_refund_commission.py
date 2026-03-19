"""
场景八：退款场景对分佣的影响
- 技师拒绝接单 -> 秒退
- 技师接单未出发 -> 人工审核
- 技师出发后 -> 不退车费，只退服务费
- 技师开始服务后 -> 不可退
"""
import allure
import jsonpath
import pytest

from config import config


@allure.epic("今夜到家分佣系统")
@allure.feature("退款对分佣影响")
class TestRefundCommission:
    """退款场景下分佣处理验证"""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-8.1 技师拒绝接单退款-秒到账")
    @allure.description("技师拒绝接单后全额退款秒到账，无分佣产生")
    def test_refund_on_reject(self, order_api, tech_api):
        with allure.step("创建订单"):
            resp = order_api.create_order(
                tech_id=config["accounts"]["technician"]["phone"],
                service_id="default_service_id",
                address="测试地址-拒单退款",
            )
            order_id = jsonpath.jsonpath(resp.json(), "$..orderId")[0]

        with allure.step("技师拒绝接单"):
            tech_api.reject_order(order_id)

        with allure.step("查询退款状态"):
            resp = order_api.get_order_detail(order_id)
            data = resp.json()

        with allure.step("验证全额退款且秒到账"):
            refund_status = jsonpath.jsonpath(data, "$..refundStatus")
            assert refund_status, "应有退款状态"
            # 秒到账 = 自动完成退款
            assert refund_status[0] in ["completed", "success", "refunded"], \
                f"拒单应秒退款，实际状态: {refund_status[0]}"

        with allure.step("验证无分佣产生"):
            resp2 = order_api.get_order_commission(order_id)
            commission = resp2.json()
            records = jsonpath.jsonpath(commission, "$..records")
            if records:
                assert len(records[0]) == 0, "拒单不应产生分佣记录"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-8.2 技师接单未出发退款-需人工审核")
    @allure.description("技师已接单但未出发，用户退款需平台人工审核")
    def test_refund_accepted_not_departed(self, order_api, tech_api,
                                          admin_api):
        with allure.step("创建订单并接单"):
            resp = order_api.create_order(
                tech_id=config["accounts"]["technician"]["phone"],
                service_id="default_service_id",
                address="测试地址-接单未出发退款",
            )
            order_id = jsonpath.jsonpath(resp.json(), "$..orderId")[0]
            tech_api.accept_order(order_id)

        with allure.step("用户申请退款"):
            refund_resp = order_api.apply_refund(order_id, refund_type="all")
            refund_data = refund_resp.json()

        with allure.step("验证退款需人工审核"):
            audit_status = jsonpath.jsonpath(refund_data, "$..auditStatus")
            assert audit_status, "应返回审核状态"
            assert audit_status[0] in ["pending", "waiting_audit"], \
                f"接单未出发退款应需人工审核，实际: {audit_status[0]}"

        with allure.step("管理员审核通过"):
            refund_id = jsonpath.jsonpath(refund_data, "$..refundId")
            if refund_id:
                admin_api.audit_refund(refund_id[0], status="approved")

        with allure.step("验证分佣记录撤销"):
            resp2 = order_api.get_order_commission(order_id)
            commission = resp2.json()
            status = jsonpath.jsonpath(commission, "$..commissionStatus")
            if status:
                assert status[0] in ["cancelled", "refunded"], \
                    "退款后分佣记录应撤销"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-8.3 技师出发后退款-只退服务费不退车费")
    @allure.description("技师已出发，用户不可退车费只能退服务费")
    def test_refund_after_departure(self, order_api, tech_api):
        with allure.step("创建订单→接单→出发"):
            resp = order_api.create_order(
                tech_id=config["accounts"]["technician"]["phone"],
                service_id="default_service_id",
                address="测试地址-出发后退款",
            )
            order_id = jsonpath.jsonpath(resp.json(), "$..orderId")[0]
            tech_api.accept_order(order_id)
            tech_api.confirm_departure(order_id)

        with allure.step("用户申请退车费"):
            travel_refund = order_api.apply_refund(
                order_id, refund_type="travel"
            )
            travel_data = travel_refund.json()

        with allure.step("验证车费不可退"):
            code = jsonpath.jsonpath(travel_data, "$.code")[0]
            assert code != 200, "技师出发后不可退车费"

        with allure.step("用户申请退服务费"):
            service_refund = order_api.apply_refund(
                order_id, refund_type="service"
            )
            service_data = service_refund.json()

        with allure.step("验证服务费可退"):
            code = jsonpath.jsonpath(service_data, "$.code")[0]
            assert code == 200, "技师出发后应可退服务费"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-8.4 技师开始服务后退款-不可退服务费")
    @allure.description("技师已开始服务，用户不能退服务费")
    def test_refund_after_service_start(self, order_api, tech_api):
        with allure.step("创建订单→接单→出发→到达→开始服务"):
            resp = order_api.create_order(
                tech_id=config["accounts"]["technician"]["phone"],
                service_id="default_service_id",
                address="测试地址-服务中退款",
            )
            order_id = jsonpath.jsonpath(resp.json(), "$..orderId")[0]
            tech_api.accept_order(order_id)
            tech_api.confirm_departure(order_id)
            tech_api.confirm_arrival(order_id)
            tech_api.start_service(order_id)

        with allure.step("用户申请退服务费"):
            refund_resp = order_api.apply_refund(
                order_id, refund_type="service"
            )
            data = refund_resp.json()

        with allure.step("验证服务费不可退"):
            code = jsonpath.jsonpath(data, "$.code")[0]
            assert code != 200, "技师开始服务后不可退服务费"
            msg = jsonpath.jsonpath(data, "$.msg")
            allure.attach(str(msg), "拒绝原因")
