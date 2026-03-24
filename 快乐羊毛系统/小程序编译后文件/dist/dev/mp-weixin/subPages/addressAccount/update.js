"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
const _sfc_main = {
  __name: "update",
  setup(__props) {
    const qqmapsdk = new common_vendor.QQMapWX({
      key: "GBWBZ-ZPOW4-LJZUG-K4U55-AFEA2-UKF5L"
    });
    const form = common_vendor.ref({
      province: "重庆市",
      address: "",
      area: "",
      lat: "",
      lng: "",
      mobile: "",
      user_name: "",
      shortCode: "",
      city: "重庆市",
      address_info: "",
      status: 0
    });
    const id = common_vendor.ref(0);
    const confirm = async () => {
      let result = id.value ? await api_common.addressModify(form.value) : await api_common.addressAdd(form.value);
      if (result.code === 200) {
        common_vendor.index.showToast({
          title: "保存成功",
          icon: "none",
          duration: 2e3,
          complete: () => {
            common_vendor.index.navigateBack();
          }
        });
      }
    };
    const onSwitchChange = (e) => {
      form.value.status = e.detail.value ? 1 : 0;
    };
    common_vendor.index.$on("city", (data) => {
      form.value.city = data.name;
    });
    common_vendor.onLoad(async (e) => {
      id.value = e.id ? e.id : 0;
      if (id.value) {
        form.value.id = id.value;
        let info = await api_common.addressInfo({ id: id.value });
        form.value = info.data;
      }
    });
    const countdown = common_vendor.ref(0);
    const getVerifyCode = async () => {
      if (!form.value.mobile) {
        common_vendor.index.showToast({ title: "请输入手机号", icon: "none" });
        return;
      }
      if (!phoneValid.value) {
        common_vendor.index.showToast({ title: "请输入正确的手机号码", icon: "none" });
        return;
      }
      try {
        await api_common.sendCode({ phone: form.value.mobile });
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
    const startCountdown = () => {
      countdown.value = 60;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
        }
      }, 1e3);
    };
    const phoneValid = common_vendor.computed(() => {
      const phoneRegex = /^1[3-9]\d{9}$/;
      return phoneRegex.test(form.value.mobile);
    });
    const selctCity = async () => {
      try {
        await new Promise((resolve, reject) => {
          common_vendor.wx$1.requirePrivacyAuthorize({
            success: resolve,
            fail: reject
          });
        });
      } catch (e) {
        common_vendor.index.showModal({
          title: "提示",
          content: "需要您授权隐私协议才能使用定位功能",
          showCancel: false
        });
        return;
      }
      common_vendor.index.showLoading({ title: "获取地址中..." });
      common_vendor.index.chooseLocation({
        success: (res) => {
          form.value.lat = res.latitude;
          form.value.lng = res.longitude;
          form.value.address = res.address || "";
          qqmapsdk.reverseGeocoder({
            location: {
              latitude: res.latitude,
              longitude: res.longitude
            },
            success: (sdkRes) => {
              common_vendor.index.hideLoading();
              if (sdkRes.status === 0 && sdkRes.result) {
                const addrComp = sdkRes.result.address_component;
                const addrFormat = sdkRes.result.formatted_addresses;
                form.value.province = addrComp.province || "";
                form.value.city = addrComp.city || "";
                form.value.area = addrComp.district || "";
                const name = addrFormat.recommend || "";
                form.value.address_info = name;
              } else {
                common_vendor.index.showToast({
                  title: "地址解析失败",
                  icon: "none"
                });
              }
            },
            fail: (err) => {
              common_vendor.index.hideLoading();
              common_vendor.index.showToast({
                title: "地址解析失败",
                icon: "none"
              });
            }
          });
        },
        fail: (err) => {
          var _a, _b;
          common_vendor.index.hideLoading();
          if ((_a = err.errMsg) == null ? void 0 : _a.includes("cancel")) {
            return;
          }
          common_vendor.index.showToast({
            title: "选择失败，请重试",
            icon: "none"
          });
          if (((_b = err.errMsg) == null ? void 0 : _b.includes("auth deny")) || err.errCode === 1505004) {
            common_vendor.index.showModal({
              title: "提示",
              content: "需要获取您的地理位置，请在小程序设置中授权",
              success: (modalRes) => {
                if (modalRes.confirm) {
                  common_vendor.index.openSetting();
                }
              }
            });
          }
        }
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.unref(form).user_name,
        b: common_vendor.o(($event) => common_vendor.unref(form).user_name = $event.detail.value),
        c: common_vendor.unref(form).mobile,
        d: common_vendor.o(($event) => common_vendor.unref(form).mobile = $event.detail.value),
        e: common_vendor.unref(form).shortCode,
        f: common_vendor.o(($event) => common_vendor.unref(form).shortCode = $event.detail.value),
        g: common_vendor.t(common_vendor.unref(countdown) > 0 ? `${common_vendor.unref(countdown)}秒后重发` : "获取验证码"),
        h: common_vendor.unref(countdown) > 0 || !common_vendor.unref(phoneValid),
        i: common_vendor.o(getVerifyCode),
        j: common_vendor.unref(countdown) > 0 || !common_vendor.unref(phoneValid) ? 1 : "",
        k: common_vendor.t(common_vendor.unref(form).address || "请选择城市"),
        l: common_vendor.o(selctCity),
        m: common_vendor.unref(form).address_info,
        n: common_vendor.o(($event) => common_vendor.unref(form).address_info = $event.detail.value),
        o: common_vendor.unref(form).status ? true : false,
        p: common_vendor.o(onSwitchChange),
        q: common_vendor.o(confirm)
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-8e3d2d8d"]]);
wx.createPage(MiniProgramPage);
