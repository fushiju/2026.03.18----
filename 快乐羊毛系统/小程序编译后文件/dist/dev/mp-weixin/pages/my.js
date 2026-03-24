"use strict";
const common_vendor = require("../common/vendor.js");
if (!Math) {
  (Icon + Navbar)();
}
const Navbar = () => "../components/NavBar/Navbar.js";
const Icon = () => "../components/Icon/Icon.js";
const _sfc_main = {
  __name: "my",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const userInfo = common_vendor.ref({
      avatarUrl: "",
      nickName: "",
      phone: "",
      id: "",
      balance: 0
    });
    common_vendor.onLoad(() => {
      const stored = common_vendor.index.getStorageSync("userInfo");
      if (stored) {
        const info = typeof stored === "string" ? JSON.parse(stored) : stored;
        userInfo.value.avatarUrl = info.avatarUrl || "";
        userInfo.value.nickName = info.nickName || "";
        userInfo.value.phone = info.phone || "";
        userInfo.value.id = info.id || info.user_id || "";
        userInfo.value.balance = info.balance || 0;
      }
    });
    const back = () => {
      common_vendor.index.navigateBack();
    };
    const handlePrice = () => {
      common_vendor.index.navigateTo({
        url: "/subPages/myPrice"
      });
    };
    const goSetting = () => {
      const autograph = common_vendor.index.getStorageSync("autograph");
      if (autograph) {
        proxy.$u.goUrl("/subPages/setting/list");
      } else {
        proxy.$u.goUrl("/subPages/login");
      }
    };
    common_vendor.onLoad(() => {
      const autograph = common_vendor.index.getStorageSync("autograph");
      if (!autograph) {
        common_vendor.index.showToast({ title: "请先登录", icon: "none" });
        setTimeout(() => {
          common_vendor.index.reLaunch({ url: "/subPages/login" });
        }, 1500);
      }
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(back),
        b: common_vendor.p({
          name: "left",
          size: 36,
          color: "#fff"
        }),
        c: common_vendor.p({
          name: "set",
          size: 36,
          color: "#fff"
        }),
        d: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/setting/list")),
        e: common_vendor.p({
          name: "message",
          size: 36,
          color: "#fff"
        }),
        f: common_vendor.p({
          backgroundColor: "#1d1e22"
        }),
        g: userInfo.value.avatarUrl || "https://pic.rmb.bdstatic.com/bjh/250325/beautify/d09d80ef2952714b3f1ec5ef2d88f4c3.jpeg?for=bg",
        h: common_vendor.t(userInfo.value.nickName || userInfo.value.phone || "未登录"),
        i: common_vendor.t(userInfo.value.id || "-"),
        j: common_vendor.o(goSetting),
        k: common_vendor.t(userInfo.value.balance),
        l: common_vendor.o(handlePrice),
        m: common_vendor.p({
          name: "daizhifu",
          size: 46,
          color: "#f38e25"
        }),
        n: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/order/list?tab=1")),
        o: common_vendor.p({
          name: "dianpulipin-fahuozhong",
          size: 46,
          color: "#f38e25"
        }),
        p: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/order/list?tab=2")),
        q: common_vendor.p({
          name: "yiwancheng",
          size: 46,
          color: "#f38e25"
        }),
        r: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/order/list?tab=7")),
        s: common_vendor.p({
          name: "tuikuanshouhou",
          size: 46,
          color: "#f38e25"
        }),
        t: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/refund/list?tab=5")),
        v: common_vendor.p({
          name: "myinfo",
          size: 46,
          color: "#f38e25"
        }),
        w: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/addressAccount/list")),
        x: common_vendor.p({
          name: "myCollect",
          size: 46,
          color: "#f38e25"
        }),
        y: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/collect")),
        z: common_vendor.p({
          name: "myCoupon",
          size: 46,
          color: "#f38e25"
        }),
        A: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/coupon/list")),
        B: common_vendor.p({
          name: "shensufankui_line",
          size: 46,
          color: "#f38e25"
        }),
        C: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/complaints/complaints")),
        D: common_vendor.p({
          name: "myCar",
          size: 46,
          color: "#f38e25"
        }),
        E: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/car")),
        F: common_vendor.p({
          name: "shangxiayou",
          size: 46,
          color: "#f38e25"
        }),
        G: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/endAgent/index")),
        H: common_vendor.p({
          name: "fenxiao",
          size: 46,
          color: "#f38e25"
        }),
        I: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/distributor/index"))
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-fd023593"]]);
wx.createPage(MiniProgramPage);
