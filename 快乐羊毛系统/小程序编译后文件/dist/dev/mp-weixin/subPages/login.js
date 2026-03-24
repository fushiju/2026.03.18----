"use strict";
const common_vendor = require("../common/vendor.js");
const api_common = require("../api/common.js");
if (!Math) {
  Checkbox();
}
const Checkbox = () => "../components/Checkbox/Checkbox.js";
const _sfc_main = {
  __name: "login",
  setup(__props) {
    let isAgree = common_vendor.ref(false);
    const userInfo = common_vendor.ref({
      avatarUrl: "",
      nickName: ""
    });
    const onGetUserInfo = (e) => {
      if (!isAgree.value) {
        common_vendor.index.showToast({
          title: "请先阅读并同意用户协议和隐私政策",
          icon: "none"
        });
        return;
      }
      if (e.detail.userInfo) {
        const { avatarUrl, nickName } = e.detail.userInfo;
        userInfo.value = {
          avatarUrl,
          nickName
        };
        common_vendor.wx$1.login({
          success: (res) => {
            if (res.code) {
              handleLogin(res.code, e.detail.userInfo);
            } else {
              common_vendor.index.showToast({
                title: "登录失败",
                icon: "none"
              });
            }
          },
          fail: () => {
            common_vendor.index.showToast({
              title: "获取登录凭证失败",
              icon: "none"
            });
          }
        });
      } else {
        common_vendor.index.showToast({
          title: "需要授权才能登录",
          icon: "none"
        });
      }
    };
    const handleLogin = async (code) => {
      try {
        const loginData = {
          code,
          appid: common_vendor.index.getAccountInfoSync().miniProgram.appId
        };
        common_vendor.index.setStorageSync("loginCode", code);
        const response = await api_common.happyLogin(loginData);
        if (response.data) {
          if (response.data.autograph) {
            common_vendor.index.setStorageSync("autograph", response.data.autograph);
          }
          if (response.data.data) {
            common_vendor.index.setStorageSync("userInfo", response.data.data);
            if (response.data.data.openid) {
              common_vendor.index.setStorageSync("openId", response.data.data.openid);
            }
          }
        }
        common_vendor.index.showToast({
          title: "登录成功",
          icon: "none"
        });
        setTimeout(() => {
          if (response && response.data && response.data.data.phone) {
            common_vendor.index.reLaunch({
              url: "/pages/index"
            });
          } else {
            common_vendor.index.navigateTo({
              url: "/subPages/bindPhone"
            });
          }
        }, 1500);
      } catch (error) {
        common_vendor.index.showToast({
          title: error.message || "登录失败",
          icon: "none"
        });
      }
    };
    const showAgreement = () => {
      common_vendor.index.showModal({
        title: "用户协议",
        content: "这里是用户协议内容...",
        showCancel: false
      });
    };
    const showPrivacy = () => {
      common_vendor.index.showModal({
        title: "隐私政策",
        content: "这里是隐私政策内容...",
        showCancel: false
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.s({
          background: common_vendor.unref(isAgree) ? "#9c8976" : "#cec8c2"
        }),
        b: common_vendor.o(onGetUserInfo),
        c: common_vendor.o(showAgreement),
        d: common_vendor.o(showPrivacy),
        e: common_vendor.o(($event) => common_vendor.isRef(isAgree) ? isAgree.value = $event : isAgree = $event),
        f: common_vendor.p({
          size: "small",
          checkedColor: "#f9be5f",
          modelValue: common_vendor.unref(isAgree)
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-9b9d0d4c"]]);
wx.createPage(MiniProgramPage);
