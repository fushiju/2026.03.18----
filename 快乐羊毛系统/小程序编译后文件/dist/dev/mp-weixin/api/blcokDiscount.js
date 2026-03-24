"use strict";
const common_request = require("../common/request.js");
function brandList(data) {
  return common_request.request.get("/massage/app/Index/typeServiceCoachList", data);
}
exports.brandList = brandList;
