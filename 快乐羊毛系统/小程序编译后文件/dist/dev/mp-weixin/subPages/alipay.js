"use strict";
const common_vendor = require("../common/vendor.js");
const api_order = require("../api/order.js");
const _sfc_main = {
  __name: "alipay",
  setup(__props) {
    const popup = common_vendor.ref();
    common_vendor.ref(false);
    const isWechatAgent = common_vendor.ref(false);
    const isHaveLink = common_vendor.ref(false);
    const link = common_vendor.ref("");
    const content = common_vendor.ref("正在支付中");
    const alipayOrderParams = common_vendor.ref({});
    const pageOptions = common_vendor.ref({});
    const isShowGuide = common_vendor.ref(true);
    const isWechat = () => {
      var ua = window.navigator.userAgent.toLowerCase();
      return "micromessenger" == ua.match(/micromessenger/i);
    };
    common_vendor.onLoad(async (options) => {
      isWechatAgent.value = isWechat();
      alipayOrderParams.value = common_vendor.index.getStorageSync("pay_list");
      pageOptions.value = options;
      link.value = `${"‘222’"}/?#/pages/pay/alipay${alipayOrderParams.value.alipay_params}`;
      common_vendor.nextTick$1(() => {
        isWechatAgent.value && popup.value.open();
        if (!isWechatAgent.value && (options == null ? void 0 : options.autograph)) {
          common_vendor.index.setStorageSync("autograph", options.autograph);
          getPayInfo();
        }
      });
    });
    const toRePay = async () => {
      var _a;
      const res = await api_order.rePayUpOrderGoods({ id: pageOptions.value.id });
      const pay_list = (_a = res.data) == null ? void 0 : _a.pay_list;
      if (pay_list) {
        if (pay_list && typeof pay_list === "object" && pay_list.id) {
          let { pay_info } = pay_list.expend;
          window.location.href = pay_info;
        } else {
          common_vendor.nextTick$1(() => {
            document.querySelector("body").innerHTML = res.data.pay_list;
            document.forms[0].submit();
          });
        }
      }
    };
    const getPayInfo = async () => {
      var _a, _b, _c, _d;
      const aliptype = ((_a = pageOptions.value) == null ? void 0 : _a.aliptype) || 0;
      if (!aliptype) {
        const res = await api_order.rePayOrder({ id: pageOptions.value.id });
        const pay_list = (_b = res.data) == null ? void 0 : _b.pay_list;
        if (pay_list) {
          if (pay_list && typeof pay_list === "object" && pay_list.id) {
            let { pay_info } = pay_list.expend;
            window.location.href = pay_info;
          } else {
            common_vendor.nextTick$1(() => {
              document.querySelector("body").innerHTML = res.data.pay_list;
              document.forms[0].submit();
            });
          }
        }
      } else if (aliptype >= 2) {
        let res;
        if (aliptype == 2) {
          res = await api_order.wechatPay({
            card_id: pageOptions.value.id,
            coach_id: pageOptions.value.coach,
            pay_model: 3
          });
        }
        if (aliptype == 3) {
          res = await api_order.agentEnd_topUp({
            cash: (_c = pageOptions.value) == null ? void 0 : _c.cash,
            pay_model: 3
          });
        }
        const pay_list = (_d = res.data) == null ? void 0 : _d.pay_list;
        if (pay_list) {
          if (pay_list && typeof pay_list === "object" && pay_list.id) {
            let { pay_info } = pay_list.expend;
            window.location.href = pay_info;
          } else {
            common_vendor.nextTick$1(() => {
              document.querySelector("body").innerHTML = res.data.pay_list;
              document.forms[0].submit();
            });
          }
        }
      }
      toRePay();
    };
    const toCopyLink = () => {
      common_vendor.index.setClipboardData({
        data: link.value,
        success() {
          common_vendor.index.showToast({
            title: "链接已复制"
          });
        }
      });
    };
    const goDetail = () => {
      const url = alipayOrderParams.value.page_url;
      if (url == "/subpages/order/list?tab=2") {
        common_vendor.index.reLaunch({
          url
        });
        return;
      }
      if (url == "/endAgent/order/list?tab=1") {
        common_vendor.index.navigateBack({
          delta: 2
        });
        return;
      }
      common_vendor.index.navigateBack();
    };
    const jump = () => {
      isHaveLink.value = true;
      isShowGuide.value = false;
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.unref(isWechatAgent)
      }, common_vendor.unref(isWechatAgent) ? common_vendor.e({
        b: common_vendor.t(common_vendor.unref(link)),
        c: common_vendor.o(toCopyLink),
        d: common_vendor.unref(isHaveLink)
      }, common_vendor.unref(isHaveLink) ? {
        e: common_vendor.o(goDetail)
      } : {}) : {
        f: common_vendor.t(common_vendor.unref(content))
      }, {
        g: common_vendor.unref(isShowGuide)
      }, common_vendor.unref(isShowGuide) ? {
        h: common_vendor.o(jump)
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-e74044c0"]]);
wx.createPage(MiniProgramPage);
