"use strict";
const common_vendor = require("../../common/vendor.js");
const api_order = require("../../api/order.js");
const api_common = require("../../api/common.js");
if (!Array) {
  const _easycom_Price2 = common_vendor.resolveComponent("Price");
  _easycom_Price2();
}
const _easycom_Price = () => "../../components/Price/Price.js";
if (!Math) {
  _easycom_Price();
}
const _sfc_main = {
  __name: "detail",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const countdown = common_vendor.ref("00:00:00");
    let timer = null;
    const formatTime = (seconds) => {
      const h = Math.floor(seconds / 3600).toString().padStart(2, "0");
      const m = Math.floor(seconds % 3600 / 60).toString().padStart(2, "0");
      const s = (seconds % 60).toString().padStart(2, "0");
      return `${h}:${m}:${s}`;
    };
    const startCountdown = (endTime) => {
      const targetTime = typeof endTime === "number" ? endTime : new Date(endTime).getTime();
      const now = Date.now();
      let remaining = Math.floor((targetTime - now) / 1e3);
      if (remaining <= 0) {
        countdown.value = "00:00:00";
        handleTimeout();
        return;
      }
      countdown.value = formatTime(remaining);
      timer = setInterval(() => {
        remaining--;
        if (remaining <= 0) {
          clearInterval(timer);
          countdown.value = "00:00:00";
          handleTimeout();
        } else {
          countdown.value = formatTime(remaining);
        }
      }, 1e3);
    };
    const handleTimeout = () => {
      common_vendor.index.showToast({
        title: "订单已超时，自动取消",
        icon: "none"
      });
    };
    const copy = (e) => {
      common_vendor.index.setClipboardData({
        data: e,
        success: function() {
          common_vendor.index.showToast({
            title: "订单号已复制",
            icon: "none",
            duration: 2e3
          });
        },
        fail: function() {
          common_vendor.index.showToast({
            title: "复制失败",
            icon: "none",
            duration: 2e3
          });
        }
      });
    };
    const orderDetail = common_vendor.ref({});
    const order_id = common_vendor.ref("");
    common_vendor.onLoad(async (options) => {
      order_id.value = options.id;
      initData();
      const orderExpireTime = options.expireTime || Date.now() + 30 * 60 * 1e3;
      startCountdown(orderExpireTime);
    });
    common_vendor.onUnmounted(() => {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    });
    const status = [
      {
        value: -1,
        label: "已取消"
      },
      {
        value: 1,
        label: "待支付"
      },
      {
        value: 2,
        label: "已支付"
      },
      {
        value: 6,
        label: "发货中"
      },
      {
        value: 7,
        label: "已完成"
      },
      {
        title: "待审核",
        value: 12
      }
    ];
    const payType = [
      {
        value: 1,
        label: "微信支付"
      },
      {
        value: 3,
        label: "支付宝支付"
      },
      {
        value: 2,
        label: "余额支付"
      }
    ];
    const getPayType = (pay_type) => {
      const item = payType.find((val) => val.value == pay_type);
      return item ? item.label : "";
    };
    const getStatus = (s) => {
      const item = status.find((val) => val.value == s);
      return item ? item.label : "";
    };
    const initData = async () => {
      const res = await api_order.orderInfo({
        id: order_id.value
      });
      orderDetail.value = res.data;
    };
    const handleCancelOrder = async (id) => {
      common_vendor.index.showModal({
        title: "提示",
        content: "确定取消订单吗？",
        success: async (res) => {
          if (res.confirm) {
            let params = {
              id
            };
            const res2 = await api_order.cancelOrder(params);
            if (res2.code === 200) {
              common_vendor.index.showToast({
                title: "取消成功",
                icon: "none"
              });
              initData();
            }
          }
        }
      });
    };
    const handlePayOrder = async (item) => {
      let params = {
        id: item.id
      };
      const result = await api_order.rePayOrder(params);
      if (result.code === 200) {
        if (item.pay_model === 1) {
          common_vendor.wx$1.requestPayment({
            provider: "wxpay",
            timeStamp: result.data.pay_list.timeStamp,
            nonceStr: result.data.pay_list.nonceStr,
            package: result.data.pay_list.package,
            signType: "MD5",
            paySign: result.data.pay_list.paySign,
            success: function(res) {
              initData();
            }
          });
        }
        if (item.pay_model === 3) {
          const pay_list_now = {
            orderInfo: result.data.data.pay_list,
            provider: "alipay"
          };
          let alipay_params = `?autograph=${common_vendor.index.getStorageSync("autograph")}&id=${result.data.order_id}`;
          const obj = Object.assign(pay_list_now, {
            order_id: result.data.order_id,
            page_url: `/subPages/order/list?tab=2`,
            alipay_params
          });
          common_vendor.index.setStorageSync("pay_list", obj);
          common_vendor.index.redirectTo({
            url: `/subPages/alipay${alipay_params}`
          });
          return;
        }
        if (result.data && item.pay_model == 2) {
          proxy.$u.toast(" 支付成功 ");
          setTimeout(() => {
            initData();
          }, 1500);
        }
      }
    };
    const handleDelOrder = async (id) => {
      common_vendor.index.showModal({
        title: "提示",
        content: "确定删除订单吗？",
        success: async (res) => {
          if (res.confirm) {
            let params = {
              id
            };
            const res2 = await api_order.delOrder(params);
            if (res2.code === 200) {
              common_vendor.index.showToast({
                title: "删除成功",
                icon: "none"
              });
              common_vendor.index.navigateBack();
            }
          }
        }
      });
    };
    const handleAgainOrder = async (e) => {
      let params = {
        order_id: e.id
      };
      const res = await api_order.againOrder(params);
      if (res.code === 200) {
        proxy.$u.goUrl(`/blockMemberRecharge/recharge?id=${e.coach_id}&title=${e.coach_info.coach_name}`);
      }
    };
    common_vendor.onShow(() => {
      initData();
    });
    const handleContact = async () => {
      const { id, pay_type } = orderDetail.value;
      if ([2, 3, 4, 5, 6].includes(pay_type)) {
        let res = await api_common.getPhone({ order_id: id });
        if (res.code !== 200)
          return useToast(res.error);
        if (!res.data)
          common_vendor.index.showToast({
            title: "稍后会有电话打入，请注意接听哦",
            icon: "none"
          });
        common_vendor.index.makePhoneCall({
          phoneNumber: res.data,
          success: (result) => {
          },
          fail: (error) => {
            useToast("拨打失败，请稍后再试");
          }
        });
      } else {
        let msg = pay_type == 7 ? "订单结束" : "订单取消";
        common_vendor.index.showToast({
          title: `${msg}不能联系客服哦`,
          icon: "none"
        });
      }
    };
    return (_ctx, _cache) => {
      var _a, _b;
      return common_vendor.e({
        a: common_vendor.t(getStatus(common_vendor.unref(orderDetail).pay_type)),
        b: common_vendor.unref(orderDetail).pay_type === 1
      }, common_vendor.unref(orderDetail).pay_type === 1 ? {
        c: common_vendor.t(common_vendor.unref(countdown))
      } : {}, {
        d: common_vendor.f(common_vendor.unref(orderDetail).order_goods, (item, index, i0) => {
          return {
            a: item.goods_cover,
            b: common_vendor.t(item.goods_name),
            c: "a3539db5-0-" + i0,
            d: index
          };
        }),
        e: common_vendor.p({
          value: common_vendor.unref(orderDetail).pay_price
        }),
        f: common_vendor.t((_a = common_vendor.unref(orderDetail).address_info) == null ? void 0 : _a.user_name),
        g: common_vendor.t((_b = common_vendor.unref(orderDetail).address_info) == null ? void 0 : _b.mobile),
        h: common_vendor.t(common_vendor.unref(orderDetail).order_code),
        i: common_vendor.o(($event) => copy(common_vendor.unref(orderDetail).order_code)),
        j: common_vendor.t(common_vendor.unref(orderDetail).create_time),
        k: common_vendor.p({
          value: common_vendor.unref(orderDetail).pay_price
        }),
        l: common_vendor.t(getPayType(common_vendor.unref(orderDetail).pay_model)),
        m: [2, 3, 4, 5, 6].includes(common_vendor.unref(orderDetail).pay_type)
      }, [2, 3, 4, 5, 6].includes(common_vendor.unref(orderDetail).pay_type) ? {
        n: common_vendor.o(handleContact)
      } : {}, {
        o: common_vendor.unref(orderDetail).pay_type == 1
      }, common_vendor.unref(orderDetail).pay_type == 1 ? {
        p: common_vendor.o(($event) => handleCancelOrder(common_vendor.unref(orderDetail).id)),
        q: common_vendor.o(($event) => handlePayOrder(common_vendor.unref(orderDetail)))
      } : {}, {
        r: common_vendor.unref(orderDetail).pay_type == -1 || common_vendor.unref(orderDetail).pay_type == 7
      }, common_vendor.unref(orderDetail).pay_type == -1 || common_vendor.unref(orderDetail).pay_type == 7 ? {
        s: common_vendor.o(($event) => handleDelOrder(common_vendor.unref(orderDetail).id))
      } : {}, {
        t: common_vendor.unref(orderDetail).can_refund > 0
      }, common_vendor.unref(orderDetail).can_refund > 0 ? {
        v: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/refund/apply?id=${common_vendor.unref(orderDetail).id}`))
      } : {}, {
        w: common_vendor.unref(orderDetail).coach_id && common_vendor.unref(orderDetail).pay_type == 7
      }, common_vendor.unref(orderDetail).coach_id && common_vendor.unref(orderDetail).pay_type == 7 ? common_vendor.e({
        x: !common_vendor.unref(orderDetail).is_comment
      }, !common_vendor.unref(orderDetail).is_comment ? {
        y: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/evaluate?id=${common_vendor.unref(orderDetail).id}`))
      } : {}, {
        z: common_vendor.unref(orderDetail).can_again
      }, common_vendor.unref(orderDetail).can_again ? {
        A: common_vendor.o(($event) => handleAgainOrder(common_vendor.unref(orderDetail)))
      } : {}) : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-a3539db5"]]);
wx.createPage(MiniProgramPage);
