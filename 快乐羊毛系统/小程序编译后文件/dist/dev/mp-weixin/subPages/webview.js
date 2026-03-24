"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  __name: "webview",
  setup(__props) {
    let srcUrl = common_vendor.ref("");
    common_vendor.onLoad((e) => {
      srcUrl.value = e.url;
      if (e.title) {
        common_vendor.index.setNavigationBarTitle({
          title: e.title
        });
      }
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.unref(srcUrl)
      };
    };
  }
};
wx.createPage(_sfc_main);
