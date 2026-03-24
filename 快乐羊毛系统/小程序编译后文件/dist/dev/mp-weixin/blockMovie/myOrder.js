"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  __name: "myOrder",
  setup(__props) {
    const autoSwitch = common_vendor.ref(true);
    const phone = common_vendor.ref("15570441314");
    const showNotice = common_vendor.ref(false);
    const isAgreed = common_vendor.ref(false);
    const handlePay = () => {
      showNotice.value = true;
      isAgreed.value = false;
    };
    const closeNoticeDialog = () => {
      showNotice.value = false;
      isAgreed.value = false;
    };
    const toggleAgree = () => {
      isAgreed.value = !isAgreed.value;
    };
    const confirmPurchase = () => {
      if (!isAgreed.value) {
        common_vendor.index.showToast({
          title: "请勾选购票须知",
          icon: "none",
          duration: 2e3
        });
        return;
      }
      closeNoticeDialog();
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: phone.value,
        b: common_vendor.o(($event) => phone.value = $event.detail.value),
        c: autoSwitch.value,
        d: common_vendor.o(($event) => autoSwitch.value = !autoSwitch.value),
        e: common_vendor.o(handlePay),
        f: showNotice.value
      }, showNotice.value ? common_vendor.e({
        g: isAgreed.value
      }, isAgreed.value ? {} : {}, {
        h: isAgreed.value ? 1 : "",
        i: common_vendor.o(toggleAgree),
        j: common_vendor.o(confirmPurchase),
        k: common_vendor.o(closeNoticeDialog),
        l: common_vendor.o(() => {
        }),
        m: common_vendor.o(closeNoticeDialog)
      }) : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-85e738d6"]]);
wx.createPage(MiniProgramPage);
