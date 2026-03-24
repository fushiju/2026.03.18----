"use strict";
const common_vendor = require("./vendor.js");
const u = {
  /*简单跳转*/
  goUrl(url) {
    common_vendor.index.navigateTo({ url });
  },
  toast(title, icon = "none") {
    common_vendor.index.showToast({
      title,
      icon
    });
  }
};
exports.u = u;
