"use strict";
const common_request = require("../common/request.js");
function partnerIndex(data) {
  return common_request.request.get("/massage/app/IndexReseller/partnerIndex", data);
}
function myteamList(data) {
  return common_request.request.get("/massage/app/IndexUser/myTeam", data);
}
function myteamEwm(data) {
  return common_request.request.get("/customer/20201", data);
}
exports.myteamEwm = myteamEwm;
exports.myteamList = myteamList;
exports.partnerIndex = partnerIndex;
