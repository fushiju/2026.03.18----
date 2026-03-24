"use strict";
const common_vendor = require("../common/vendor.js");
const api_my = require("../api/my.js");
if (!Math) {
  (Icon + RechargeTab + ConsumeTab)();
}
const Icon = () => "../components/Icon/Icon.js";
const RechargeTab = () => "../pages/components/RechargeTab.js";
const ConsumeTab = () => "../pages/components/ConsumeTab.js";
const _sfc_main = {
  __name: "myPrice",
  setup(__props) {
    const activeTab = common_vendor.ref(0);
    const rechargeAmount = common_vendor.ref(300);
    const selectedPackage = common_vendor.ref(0);
    const payList = common_vendor.ref([]);
    const myprice = common_vendor.ref({ balance: 0 });
    const moyleList = common_vendor.ref([]);
    const allPay = [
      {
        id: 3,
        icon: "aliPay",
        name: "支付宝支付",
        ischeck: false,
        closeKey: "close_alipay"
      },
      {
        id: 1,
        icon: "weChatPay",
        name: "微信支付",
        ischeck: false,
        closeKey: "close_wxpay"
      }
    ];
    const priceList = async () => {
      const res = await api_my.IndexUser();
      myprice.value = res.data;
    };
    const selectPackage = (index, amount) => {
      selectedPackage.value = index;
      rechargeAmount.value = amount;
    };
    const handleSelectPackage = (index, amount) => {
      selectPackage(index, amount);
    };
    const getcardList = async () => {
      try {
        const res = await api_my.cardList();
        moyleList.value = res.data.data;
        if (moyleList.value.length > 0) {
          selectedPackage.value = 0;
          rechargeAmount.value = moyleList.value[0].price;
        }
      } catch (error) {
      }
    };
    const handleRecharge = async () => {
      const selectedCard = moyleList.value[selectedPackage.value];
      if (!selectedCard) {
        common_vendor.index.showToast({ title: "请选择充值套餐", icon: "none" });
        return;
      }
      const selectedPay = payList.value.find((item) => item.ischeck);
      if (!selectedPay) {
        common_vendor.index.showToast({ title: "请选择支付方式", icon: "none" });
        return;
      }
      let params = {
        card_id: String(selectedCard.id),
        // 套餐ID
        coach_id: "0",
        // 默认0
        pay_model: selectedPay.id
        //  (1:微信, 2:余额, 3:支付宝)
      };
      try {
        common_vendor.index.showLoading({ title: "正在发起支付..." });
        const res = await api_my.recharge(params);
        common_vendor.index.hideLoading();
        if (params.pay_model === 1) {
        } else if (params.pay_model === 3) {
        } else {
          common_vendor.index.showToast({ title: "充值成功" });
          priceList();
        }
      } catch (error) {
        common_vendor.index.hideLoading();
        common_vendor.index.showToast({ title: "支付失败", icon: "none" });
      }
    };
    const selPay = (index) => {
      if (!payList.value[index])
        return;
      payList.value.forEach((item) => item.ischeck = false);
      payList.value[index].ischeck = true;
    };
    const handlePaySelect = (index) => {
      selPay(index);
    };
    common_vendor.onLoad(() => {
      const setting = common_vendor.index.getStorageSync("config") || {};
      const filtered = allPay.filter((item) => setting[item.closeKey] === 0).map((item) => ({ ...item }));
      if (filtered.length > 0) {
        filtered[0].ischeck = true;
      }
      payList.value = filtered;
    });
    common_vendor.onMounted(() => {
      priceList();
      getcardList();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.t(myprice.value.balance),
        b: activeTab.value === 0 ? 1 : "",
        c: common_vendor.o(($event) => activeTab.value = 0),
        d: activeTab.value === 1 ? 1 : "",
        e: common_vendor.o(($event) => activeTab.value = 1),
        f: activeTab.value === 2 ? 1 : "",
        g: common_vendor.o(($event) => activeTab.value = 2),
        h: activeTab.value === 0
      }, activeTab.value === 0 ? {
        i: common_vendor.f(moyleList.value, (item, index, i0) => {
          return {
            a: common_vendor.t(item.price),
            b: common_vendor.t(item.title),
            c: item.id || index,
            d: selectedPackage.value === index ? 1 : "",
            e: common_vendor.o(($event) => handleSelectPackage(index, item.price), item.id || index)
          };
        }),
        j: common_vendor.f(payList.value, (item, index, i0) => {
          return {
            a: "64ee037c-0-" + i0,
            b: common_vendor.p({
              name: item.icon,
              color: "#f9be5f",
              size: "48rpx"
            }),
            c: common_vendor.t(item.name),
            d: "64ee037c-1-" + i0,
            e: common_vendor.p({
              name: item.ischeck ? "xuanzhongduigou" : "check_normal",
              size: "40rpx",
              color: item.ischeck ? "#ff471f" : "#ccc"
            }),
            f: item.id,
            g: item.ischeck ? 1 : "",
            h: common_vendor.o(($event) => handlePaySelect(index), item.id)
          };
        })
      } : {}, {
        k: activeTab.value === 1
      }, activeTab.value === 1 ? {} : {}, {
        l: activeTab.value === 2
      }, activeTab.value === 2 ? {} : {}, {
        m: activeTab.value === 0
      }, activeTab.value === 0 ? {
        n: common_vendor.t(rechargeAmount.value),
        o: common_vendor.o(handleRecharge)
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-64ee037c"]]);
wx.createPage(MiniProgramPage);
