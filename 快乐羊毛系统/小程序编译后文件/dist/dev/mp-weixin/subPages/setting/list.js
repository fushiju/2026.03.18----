"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Math) {
  Icon();
}
const Icon = () => "../../components/Icon/Icon.js";
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const userInfo = common_vendor.ref({
      avatarUrl: "",
      nickName: "",
      phone: "",
      id: ""
    });
    common_vendor.onLoad(() => {
      const stored = common_vendor.index.getStorageSync("userInfo");
      if (stored) {
        const info = typeof stored === "string" ? JSON.parse(stored) : stored;
        userInfo.value.avatarUrl = info.avatarUrl || "";
        userInfo.value.nickName = info.nickName || "";
        userInfo.value.phone = info.phone || "";
        userInfo.value.id = info.id || info.user_id || "";
      }
    });
    const handlelogout = () => {
      common_vendor.index.showModal({
        title: "提示",
        content: "确定要退出登录吗？",
        success: (res) => {
          if (res.confirm) {
            common_vendor.index.removeStorageSync("autograph");
            common_vendor.index.removeStorageSync("userInfo");
            common_vendor.index.removeStorageSync("openId");
            common_vendor.index.reLaunch({
              url: "/pages/index"
            });
          }
        }
      });
    };
    return (_ctx, _cache) => {
      return {
        a: userInfo.value.avatarUrl || "https://pic.rmb.bdstatic.com/bjh/250325/beautify/d09d80ef2952714b3f1ec5ef2d88f4c3.jpeg?for=bg",
        b: common_vendor.t(userInfo.value.nickName || userInfo.value.phone || "未登录"),
        c: common_vendor.t(userInfo.value.id || "-"),
        d: common_vendor.p({
          name: "right",
          size: 36,
          color: "#ccc"
        }),
        e: common_vendor.p({
          name: "right",
          size: 36,
          color: "#ccc"
        }),
        f: common_vendor.p({
          name: "right",
          size: 36,
          color: "#ccc"
        }),
        g: common_vendor.o(handlelogout)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-c078ee0d"]]);
wx.createPage(MiniProgramPage);
