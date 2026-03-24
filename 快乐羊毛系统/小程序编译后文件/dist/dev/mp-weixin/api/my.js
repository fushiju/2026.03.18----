"use strict";
const common_request = require("../common/request.js");
function IndexUser() {
  return common_request.request.get("/customer/20190");
}
function cardList() {
  return common_request.request.get("/customer/20050");
}
function recharge(data) {
  return common_request.request.post("/customer/20052", data);
}
function rechargeRecord(data) {
  return common_request.request.get("/customer/20049", data);
}
function consumptionRecord(data) {
  return common_request.request.get("/customer/20053", data);
}
function orderInfo(data) {
  return common_request.request.get("/customer/20133", data);
}
function orderDetail(data) {
  return common_request.request.get("/customer/20132", data);
}
function orderStatusDetail(data) {
  return common_request.request.get("/customer/20125", data);
}
function cancelRefundOrder(data) {
  return common_request.request.post("/customer/20113", data);
}
exports.IndexUser = IndexUser;
exports.cancelRefundOrder = cancelRefundOrder;
exports.cardList = cardList;
exports.consumptionRecord = consumptionRecord;
exports.orderDetail = orderDetail;
exports.orderInfo = orderInfo;
exports.orderStatusDetail = orderStatusDetail;
exports.recharge = recharge;
exports.rechargeRecord = rechargeRecord;
