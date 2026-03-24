"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
const _sfc_main = {
  __name: "detail",
  setup(__props) {
    const detail = common_vendor.ref({});
    common_vendor.onLoad(async (e) => {
      let res = await api_common.feedbackDetail({ id: e.id });
      if (res.code === 200)
        detail.value = res.data;
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.t(common_vendor.unref(detail).type_name),
        b: common_vendor.t(common_vendor.unref(detail).order_code),
        c: common_vendor.t(common_vendor.unref(detail).content),
        d: common_vendor.f(common_vendor.unref(detail).images, (i, k0, i0) => {
          return {
            a: i
          };
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-aa7cdea3"]]);
wx.createPage(MiniProgramPage);
