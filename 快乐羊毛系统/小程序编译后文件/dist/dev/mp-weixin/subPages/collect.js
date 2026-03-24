"use strict";
const common_vendor = require("../common/vendor.js");
const api_common = require("../api/common.js");
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  _easycom_Icon2();
}
const _easycom_Icon = () => "../components/Icon/Icon.js";
if (!Math) {
  _easycom_Icon();
}
const _sfc_main = {
  __name: "collect",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const collectList = common_vendor.ref([]);
    const collect = async (item) => {
      const p = {
        coach_id: item.id
      };
      let res = await api_common.delCollect(p);
      if (res.code == 200)
        common_vendor.index.showToast({
          title: "取消收藏",
          icon: "none",
          duration: 1500,
          complete: () => {
            initData();
          }
        });
    };
    const initData = async () => {
      const params = {
        page: 1,
        ser_id: 0,
        coach_name: "",
        lat: 29.715146,
        lng: 106.634171
      };
      let res = await api_common.myCollect(params);
      collectList.value = res.data.data;
    };
    common_vendor.onLoad(() => {
      initData();
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(common_vendor.unref(collectList), (item, index, i0) => {
          return {
            a: item.work_img,
            b: common_vendor.t(item.coach_name),
            c: "7c26c8ea-0-" + i0,
            d: common_vendor.p({
              name: item.collect_num ? "myCollect-full" : "myCollect",
              size: item.collect_num ? "44rpx" : "46rpx",
              color: item.collect_num ? "#ff0000" : "#bababa"
            }),
            e: common_vendor.o(($event) => collect(item), index),
            f: common_vendor.t(item.text),
            g: index,
            h: common_vendor.o(($event) => {
              common_vendor.unref(proxy).$u.goUrl(`/blockMemberRecharge/recharge?id=${item.id}&title=${item.coach_name}`);
            }, index)
          };
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-7c26c8ea"]]);
wx.createPage(MiniProgramPage);
