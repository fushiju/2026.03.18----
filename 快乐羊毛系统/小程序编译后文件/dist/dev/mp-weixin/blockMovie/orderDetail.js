"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  __name: "orderDetail",
  setup(__props) {
    const orderNo = common_vendor.ref("202603071707513938");
    const copyOrderNo = () => {
      common_vendor.index.setClipboardData({
        data: orderNo.value,
        success: () => {
          common_vendor.index.showToast({
            title: "复制成功",
            icon: "success",
            duration: 2e3
          });
        },
        fail: () => {
          common_vendor.index.showToast({
            title: "复制失败",
            icon: "none",
            duration: 2e3
          });
        }
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.t(orderNo.value),
        b: common_vendor.o(copyOrderNo)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-2761906a"]]);
wx.createPage(MiniProgramPage);
