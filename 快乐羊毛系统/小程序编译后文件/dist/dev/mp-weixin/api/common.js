"use strict";
const common_request = require("../common/request.js");
function configInfo() {
  return common_request.request.get("customer/20026");
}
function orderList(data) {
  return common_request.request.get("customer/20126", data);
}
function addressList() {
  return common_request.request.get("customer/20159");
}
function addressAdd(data) {
  return common_request.request.post("customer/20156", data);
}
function addressDelete(data) {
  return common_request.request.post("customer/20157", data);
}
function addressInfo(data) {
  return common_request.request.get("customer/20158", data);
}
function addressModify(data) {
  return common_request.request.post("customer/20160", data);
}
function happyLogin(data) {
  return common_request.request.post("/massage/app/index/happyLogin", {
    code: data.code || "",
    appid: data.appid || ""
  }, {
    showLoading: true,
    loadingText: "登录中..."
  });
}
function sendCode(data) {
  return common_request.request.post("/customer/20195", data);
}
function bindPhone(data) {
  return common_request.request.post("/customer/20172", data);
}
function evaList() {
  return common_request.request.get("customer/20123");
}
function getPhone(data) {
  return common_request.request.post("customer/20090", data);
}
function feedback(data) {
  return common_request.request.post("customer/20063", data);
}
function feedbackList(data) {
  return common_request.request.get("customer/20094", data);
}
function feedbackDetail(data) {
  return common_request.request.get("customer/20086", data);
}
function getCouponList(data) {
  return common_request.request.get("customer/20202", data);
}
function getUserCouponList(data) {
  return common_request.request.get("customer/20115", data);
}
function couponDel(data) {
  return common_request.request.post("customer/20181", data);
}
function myCollect(data) {
  return common_request.request.get("customer/20178", data);
}
function addCollect(data) {
  return common_request.request.post("customer/20154", data);
}
function delCollect(data) {
  return common_request.request.post("customer/20182", data);
}
exports.addCollect = addCollect;
exports.addressAdd = addressAdd;
exports.addressDelete = addressDelete;
exports.addressInfo = addressInfo;
exports.addressList = addressList;
exports.addressModify = addressModify;
exports.bindPhone = bindPhone;
exports.configInfo = configInfo;
exports.couponDel = couponDel;
exports.delCollect = delCollect;
exports.evaList = evaList;
exports.feedback = feedback;
exports.feedbackDetail = feedbackDetail;
exports.feedbackList = feedbackList;
exports.getCouponList = getCouponList;
exports.getPhone = getPhone;
exports.getUserCouponList = getUserCouponList;
exports.happyLogin = happyLogin;
exports.myCollect = myCollect;
exports.orderList = orderList;
exports.sendCode = sendCode;
