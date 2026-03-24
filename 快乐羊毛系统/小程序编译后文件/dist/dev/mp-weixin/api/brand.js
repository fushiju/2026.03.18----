"use strict";
const common_request = require("../common/request.js");
function brandList(data) {
  return common_request.request.get("/customer/20045", data);
}
function getSpecificationList(data) {
  return common_request.request.get("/customer/20024", data);
}
function brandListinfo(data) {
  return common_request.request.get("/customer/20023", data);
}
exports.brandList = brandList;
exports.brandListinfo = brandListinfo;
exports.getSpecificationList = getSpecificationList;
