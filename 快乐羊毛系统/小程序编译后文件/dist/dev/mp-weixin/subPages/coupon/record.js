"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Math) {
  (Icon + Navbar + Tabs + Price)();
}
const Navbar = () => "../../components/NavBar/Navbar.js";
const Icon = () => "../../components/Icon/Icon.js";
const Tabs = () => "../../components/Tabs/Tabs.js";
const Price = () => "../../components/Price/Price.js";
const _sfc_main = {
  __name: "record",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const handleTabClick = (index) => {
      status.value = index;
    };
    const status = common_vendor.ref(0);
    const backUrl = () => {
      common_vendor.index.navigateBack();
    };
    const couponList = common_vendor.ref([
      {
        id: 1,
        name: "测试名称",
        price: "5",
        desc: "测试描述",
        title: "测试标题",
        tag: "快过期",
        time: "2022-02-02-2023-02-02",
        detail: "测试详情",
        isShowOtherInfo: false
      },
      {
        id: 2,
        name: "测试名称",
        price: "5",
        desc: "测试描述",
        title: "测试标题",
        tag: "新到",
        time: "2022-02-02-2023-02-02",
        detail: "测试详情",
        isShowOtherInfo: false
      }
    ]);
    const toggleOtherInfo = (index) => {
      couponList.value[index].isShowOtherInfo = !couponList.value[index].isShowOtherInfo;
    };
    const couponType = common_vendor.ref([
      {
        title: "已使用",
        value: 0
      },
      {
        title: "已使用",
        value: 1
      }
    ]);
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(backUrl),
        b: common_vendor.p({
          name: "left",
          size: "56rpx"
        }),
        c: common_vendor.p({
          fixed: true,
          title: "优惠券"
        }),
        d: common_vendor.o(handleTabClick),
        e: common_vendor.p({
          tabs: common_vendor.unref(couponType),
          ["v-modelValue"]: common_vendor.unref(status),
          scrollable: true,
          activeColor: "#f9be5f",
          inactiveColor: "#ccc",
          fontSize: 24
        }),
        f: common_vendor.f(common_vendor.unref(couponList), (item, index, i0) => {
          return {
            a: "194cef6b-3-" + i0,
            b: "194cef6b-4-" + i0,
            c: common_vendor.p({
              value: item.price,
              size: "36",
              color: "#adabab"
            }),
            d: common_vendor.t(item.desc),
            e: common_vendor.t(item.title),
            f: common_vendor.t(item.time),
            g: "194cef6b-5-" + i0,
            h: common_vendor.p({
              name: item.isShowOtherInfo ? "up" : "down",
              size: "36rpx",
              color: "#adabab"
            }),
            i: common_vendor.s({
              "border-radius": item.isShowOtherInfo ? "0" : "16rpx"
            }),
            j: common_vendor.o(($event) => toggleOtherInfo(index), index),
            k: common_vendor.t(item.detail),
            l: item.isShowOtherInfo,
            m: index
          };
        }),
        g: common_vendor.p({
          name: "used",
          size: "80rpx",
          color: "#adabab"
        }),
        h: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/coupon/list"))
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-194cef6b"]]);
wx.createPage(MiniProgramPage);
