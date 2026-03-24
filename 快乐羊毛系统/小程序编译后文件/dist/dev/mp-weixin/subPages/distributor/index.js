"use strict";
const common_vendor = require("../../common/vendor.js");
const api_distributor = require("../../api/distributor.js");
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const performanceData = common_vendor.ref({});
    const getpartner = async () => {
      const res = await api_distributor.partnerIndex();
      performanceData.value = res.data;
    };
    const goToEarnings = () => {
      common_vendor.index.navigateTo({
        url: "/subPages/distributor/myMembers"
      });
    };
    common_vendor.onMounted(() => {
      getpartner();
    });
    return (_ctx, _cache) => {
      var _a, _b, _c, _d, _e, _f, _g, _h;
      return {
        a: performanceData.value.avatarUrl,
        b: common_vendor.t(performanceData.value.nickName || performanceData.value.phone),
        c: common_vendor.t(performanceData.value.adminName || "暂无"),
        d: common_vendor.t(((_a = performanceData.value) == null ? void 0 : _a.orderCommCash) || 0),
        e: common_vendor.t(((_b = performanceData.value) == null ? void 0 : _b.totalOrderCount) || 0),
        f: common_vendor.t(((_c = performanceData.value) == null ? void 0 : _c.notRecorded) || 0),
        g: common_vendor.t(((_d = performanceData.value) == null ? void 0 : _d.totalOrderCount) || 0),
        h: common_vendor.t(((_e = performanceData.value) == null ? void 0 : _e.todayOrderCount) || 0),
        i: common_vendor.t(((_f = performanceData.value) == null ? void 0 : _f.totalUserCount) || 0),
        j: common_vendor.t(((_g = performanceData.value) == null ? void 0 : _g.todayUserCount) || 0),
        k: common_vendor.t(((_h = performanceData.value) == null ? void 0 : _h.walletCash) || 0),
        l: common_vendor.o(goToEarnings),
        m: common_vendor.o(($event) => common_vendor.index.navigateTo({
          url: "/subPages/distributor/invitation"
        }))
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-44bf8298"]]);
wx.createPage(MiniProgramPage);
