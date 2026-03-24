"use strict";
const common_request = require("../common/request.js");
function rePayOrder(data) {
  return common_request.request.post("/customer/20130", data);
}
function addCar(data) {
  return common_request.request.post("/customer/20018", data);
}
function delCar(data) {
  return common_request.request.post("/customer/20028", data);
}
function payOrder(data) {
  return common_request.request.post("/customer/20127", data);
}
function rePayUpOrderGoods(data) {
  return common_request.request.post("/customer/20131", data);
}
function wechatPay(data) {
  return common_request.request.post("/customer/20052", data);
}
function agentEnd_topUp(data) {
  return common_request.request.post("/customer/20253", data);
}
function payOrderInfo(data) {
  return common_request.request.get("/customer/20128", data);
}
function payOrderInfoConfig(data) {
  return common_request.request.get("/customer/20129", data);
}
function orderInfo(data) {
  return common_request.request.get("/customer/20125", data);
}
function refundOrder(data) {
  return common_request.request.post("/customer/20110", data);
}
function cancelOrder(data) {
  return common_request.request.post("/customer/20112", data);
}
function delOrder(data) {
  return common_request.request.post("/customer/20117", data);
}
function againOrder(data) {
  return common_request.request.post("/customer/20039", data);
}
function evaOrder(data) {
  return common_request.request.post("/customer//20109", data);
}
exports.addCar = addCar;
exports.againOrder = againOrder;
exports.agentEnd_topUp = agentEnd_topUp;
exports.cancelOrder = cancelOrder;
exports.delCar = delCar;
exports.delOrder = delOrder;
exports.evaOrder = evaOrder;
exports.orderInfo = orderInfo;
exports.payOrder = payOrder;
exports.payOrderInfo = payOrderInfo;
exports.payOrderInfoConfig = payOrderInfoConfig;
exports.rePayOrder = rePayOrder;
exports.rePayUpOrderGoods = rePayUpOrderGoods;
exports.refundOrder = refundOrder;
exports.wechatPay = wechatPay;
