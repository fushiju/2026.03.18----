"use strict";
const common_vendor = require("../common/vendor.js");
const api_common = require("../api/common.js");
if (!Math) {
  (Icon + Navbar)();
}
const Navbar = () => "../components/NavBar/Navbar.js";
const Icon = () => "../components/Icon/Icon.js";
const _sfc_main = {
  __name: "bindPhone",
  setup(__props) {
    const phone = common_vendor.ref("");
    const verifyCode = common_vendor.ref("");
    const countdown = common_vendor.ref(0);
    const phoneValid = common_vendor.computed(() => {
      const phoneRegex = /^1[3-9]\d{9}$/;
      return phoneRegex.test(phone.value);
    });
    const canSubmit = common_vendor.computed(() => {
      return phoneValid.value && verifyCode.value.length === 6;
    });
    const startCountdown = () => {
      countdown.value = 60;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
        }
      }, 1e3);
    };
    const getVerifyCode = async () => {
      if (!phone.value) {
        common_vendor.index.showToast({ title: "请输入手机号", icon: "none" });
        return;
      }
      if (!phoneValid.value) {
        common_vendor.index.showToast({ title: "请输入正确的手机号码", icon: "none" });
        return;
      }
      try {
        await api_common.sendCode({ phone: phone.value });
        common_vendor.index.showToast({
          title: "验证码已发送",
          icon: "none"
        });
        startCountdown();
      } catch (error) {
        common_vendor.index.showToast({
          title: error.message || "验证码发送失败",
          icon: "none",
          duration: 2e3
        });
      }
    };
    const submitBind = async () => {
      if (!canSubmit.value)
        return;
      common_vendor.index.showLoading({
        title: "绑定中..."
      });
      try {
        const res = await api_common.bindPhone({
          phone: phone.value,
          shortCode: verifyCode.value
        });
        try {
          const loginRes = await api_common.happyLogin({
            code: common_vendor.index.getStorageSync("loginCode") || "",
            appid: common_vendor.index.getAccountInfoSync().miniProgram.appId
          });
          if (loginRes.data) {
            if (loginRes.data.autograph) {
              common_vendor.index.setStorageSync("autograph", loginRes.data.autograph);
            }
            if (loginRes.data.data) {
              common_vendor.index.setStorageSync("userInfo", loginRes.data.data);
              if (loginRes.data.data.openid) {
                common_vendor.index.setStorageSync("openId", loginRes.data.data.openid);
              }
            }
          }
        } catch (loginError) {
        }
        common_vendor.index.hideLoading();
        common_vendor.index.showToast({
          title: "绑定成功",
          icon: "none"
        });
        setTimeout(() => {
          common_vendor.index.reLaunch({
            url: "/pages/my"
          });
        }, 1500);
      } catch (error) {
        common_vendor.index.hideLoading();
        common_vendor.index.showToast({
          title: error.message || "绑定失败",
          icon: "none",
          duration: 2e3
        });
      }
    };
    const backUrl = () => {
      common_vendor.index.navigateBack();
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(backUrl),
        b: common_vendor.p({
          name: "left",
          size: "48rpx"
        }),
        c: common_vendor.p({
          fixed: true,
          ["safe-area-inset-top"]: true
        }),
        d: common_vendor.unref(phone),
        e: common_vendor.o(($event) => common_vendor.isRef(phone) ? phone.value = $event.detail.value : null),
        f: common_vendor.unref(phone).length > 0 && !common_vendor.unref(phoneValid)
      }, common_vendor.unref(phone).length > 0 && !common_vendor.unref(phoneValid) ? {} : {}, {
        g: common_vendor.unref(verifyCode),
        h: common_vendor.o(($event) => common_vendor.isRef(verifyCode) ? verifyCode.value = $event.detail.value : null),
        i: common_vendor.t(common_vendor.unref(countdown) > 0 ? `${common_vendor.unref(countdown)}秒后重发` : "获取验证码"),
        j: common_vendor.unref(countdown) > 0 || !common_vendor.unref(phoneValid),
        k: common_vendor.o(getVerifyCode),
        l: common_vendor.unref(countdown) > 0 || !common_vendor.unref(phoneValid) ? 1 : "",
        m: common_vendor.o(submitBind),
        n: !common_vendor.unref(canSubmit),
        o: !common_vendor.unref(canSubmit) ? 1 : ""
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-fd8f65c4"]]);
wx.createPage(MiniProgramPage);
