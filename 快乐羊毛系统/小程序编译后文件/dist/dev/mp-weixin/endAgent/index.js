"use strict";
const common_vendor = require("../common/vendor.js");
const api_endAgent = require("../api/endAgent.js");
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  _easycom_Icon2();
}
const _easycom_Icon = () => "../components/Icon/Icon.js";
if (!Math) {
  _easycom_Icon();
}
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const userInfo = common_vendor.ref({});
    const getInfo = async () => {
      const res = await api_endAgent.agentUserInfo();
      console.log(res, "哈哈哈哈哈");
      userInfo.value = res.data;
    };
    common_vendor.onMounted(() => {
      getInfo();
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.t(common_vendor.unref(userInfo).cash),
        b: common_vendor.t(common_vendor.unref(userInfo).total_cash),
        c: common_vendor.p({
          name: "myOrder",
          size: 46,
          color: "#f38e25"
        }),
        d: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/order/list?tab=1")),
        e: common_vendor.p({
          name: "myOrder",
          size: 46,
          color: "#f38e25"
        }),
        f: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/order/list?tab=6")),
        g: common_vendor.p({
          name: "myOrder",
          size: 46,
          color: "#f38e25"
        }),
        h: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/order/list?tab=7")),
        i: common_vendor.p({
          name: "myOrder",
          size: 46,
          color: "#f38e25"
        }),
        j: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/order/list?tab=12")),
        k: common_vendor.p({
          name: "myOrder",
          size: 46,
          color: "#f38e25"
        }),
        l: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/order/ordertui?tab=0")),
        m: common_vendor.p({
          name: "myCollect",
          size: 46,
          color: "#f38e25"
        }),
        n: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/addBrand/list")),
        o: common_vendor.p({
          name: "myCollect",
          size: 46,
          color: "#f38e25"
        }),
        p: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/agent/index")),
        q: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/agent/index"))
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-3faf6778"]]);
wx.createPage(MiniProgramPage);
