"use strict";
const common_vendor = require("../common/vendor.js");
const common_request = require("../common/request.js");
function agentUserInfo(data) {
  return common_request.request.get("/customer/20243", data);
}
function agentInvresellerQr(data) {
  return common_request.request.get("/customer/20231", data);
}
function agentImg(data) {
  return common_request.request.get("/customer/20243", data);
}
function agentStatus(data) {
  return common_request.request.get("/customer/20249", data);
}
function agentTk(data) {
  return common_request.request.get("/customer/20255", data);
}
function agentBrandList(data) {
  return common_request.request.get("/customer/20237", data);
}
function agentQd(data) {
  return common_request.request.get("/customer/20179", data);
}
function agentBrandCity(data) {
  return common_request.request.get("/customer/20241", data);
}
function coachTypeSelect(data) {
  return common_request.request.get("/mobilenode/app/IndexAgentOrder/coachTypeSelect", data);
}
function agentAddBrand(data) {
  return common_request.request.post("/customer/20235", data);
}
function agentEditBrand(data) {
  return common_request.request.post("/customer/20238", data);
}
function agentViewBrand(data) {
  return common_request.request.get("/customer/20236", data);
}
const BASE_URL = "https://red.jinyedaojia.com/";
function upLoadImg(tempFilePath, typeData) {
  return new Promise((resolve, reject) => {
    common_vendor.index.uploadFile({
      url: BASE_URL + "/customer/20005",
      filePath: tempFilePath,
      // 这必须是一个字符串路径！
      name: "file",
      // 后端接收文件的字段名，一般是 file
      formData: {
        "type": typeData
        // 1 或 3
      },
      header: {
        "autograph": common_vendor.index.getStorageSync("autograph")
      },
      success: (res) => {
        const data = JSON.parse(res.data);
        if (data.code === 200) {
          resolve(data);
        } else {
          common_vendor.index.showToast({ title: data.return_msg || "上传失败", icon: "none" });
          reject(data);
        }
      },
      fail: (err) => {
        common_vendor.index.showToast({ title: "网络上传失败", icon: "none" });
        reject(err);
      }
    });
  });
}
exports.agentAddBrand = agentAddBrand;
exports.agentBrandCity = agentBrandCity;
exports.agentBrandList = agentBrandList;
exports.agentEditBrand = agentEditBrand;
exports.agentImg = agentImg;
exports.agentInvresellerQr = agentInvresellerQr;
exports.agentQd = agentQd;
exports.agentStatus = agentStatus;
exports.agentTk = agentTk;
exports.agentUserInfo = agentUserInfo;
exports.agentViewBrand = agentViewBrand;
exports.coachTypeSelect = coachTypeSelect;
exports.upLoadImg = upLoadImg;
