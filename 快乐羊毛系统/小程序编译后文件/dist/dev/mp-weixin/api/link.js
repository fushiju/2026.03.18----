"use strict";
const common_request = require("../common/request.js");
function categroy(data) {
  return common_request.request.get("massage/app/goods/categoryList", data);
}
function goodsList(data) {
  return common_request.request.get("/massage/app/goods/goodsApiList", data);
}
exports.categroy = categroy;
exports.goodsList = goodsList;
