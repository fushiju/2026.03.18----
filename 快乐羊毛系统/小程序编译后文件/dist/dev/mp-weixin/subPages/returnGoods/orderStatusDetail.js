"use strict";
const common_vendor = require("../../common/vendor.js");
const api_my = require("../../api/my.js");
const _sfc_main = {
  __name: "orderStatusDetail",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const countdown = common_vendor.ref("00:00:00");
    let timer = null;
    const loading = common_vendor.ref(false);
    const detail = common_vendor.ref(null);
    const orderCode = common_vendor.ref("");
    const statusMap = {
      1: { label: "待付款", color: "#ff9800", desc: "订单待支付，请尽快完成付款" },
      2: { label: "发货中", color: "#2196f3", desc: "商家正在为您备货发货" },
      5: { label: "待收货", color: "#4caf50", desc: "商品已发出，请注意查收" },
      7: { label: "已完成", color: "#9e9e9e", desc: "订单已完成，感谢您的惠顾" }
    };
    const currentStatus = common_vendor.ref(1);
    const statusInfo = common_vendor.computed(() => statusMap[currentStatus.value] || statusMap[1]);
    const getDetail = async (id) => {
      var _a;
      loading.value = true;
      try {
        const res = await api_my.orderStatusDetail({ id });
        if (res.data) {
          detail.value = res.data;
          if (res.data.pay_type) {
            currentStatus.value = Number(res.data.pay_type);
          }
          if (res.data.add_order_id && res.data.add_order_id.length > 0) {
            orderCode.value = ((_a = res.data.add_order_id[0]) == null ? void 0 : _a.order_code) || "";
          }
        }
      } catch (e) {
        common_vendor.index.showToast({ title: "加载失败，请重试", icon: "none" });
      } finally {
        loading.value = false;
      }
    };
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
        return;
      }
      countdown.value = formatTime(remaining);
      timer = setInterval(() => {
        remaining--;
        if (remaining <= 0) {
          clearInterval(timer);
          countdown.value = "00:00:00";
        } else {
          countdown.value = formatTime(remaining);
        }
      }, 1e3);
    };
    const copy = (text) => {
      common_vendor.index.setClipboardData({
        data: String(text),
        success() {
          common_vendor.index.showToast({ title: "已复制", icon: "none", duration: 2e3 });
        },
        fail() {
          common_vendor.index.showToast({ title: "复制失败", icon: "none", duration: 2e3 });
        }
      });
    };
    common_vendor.onLoad((options) => {
      if (options.pay_type) {
        currentStatus.value = Number(options.pay_type);
      }
      if (options.id) {
        getDetail(options.id);
      }
      const orderExpireTime = options.expireTime || Date.now() + 30 * 60 * 1e3;
      startCountdown(orderExpireTime);
    });
    common_vendor.onUnmounted(() => {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.t(statusInfo.value.label),
        b: common_vendor.t(statusInfo.value.desc),
        c: statusInfo.value.color,
        d: loading.value
      }, loading.value ? {} : detail.value ? common_vendor.e({
        f: common_vendor.f(detail.value.order_goods, (goods, k0, i0) => {
          return {
            a: goods.goods_cover,
            b: common_vendor.t(goods.goods_name),
            c: common_vendor.t(goods.num),
            d: common_vendor.t(goods.goods_price),
            e: goods.id
          };
        }),
        g: detail.value.address_info
      }, detail.value.address_info ? {
        h: common_vendor.t(detail.value.address_info.user_name),
        i: common_vendor.t(detail.value.address_info.mobile),
        j: common_vendor.t(detail.value.address_info.province),
        k: common_vendor.t(detail.value.address_info.city),
        l: common_vendor.t(detail.value.address_info.area),
        m: common_vendor.t(detail.value.address_info.address),
        n: common_vendor.t(detail.value.address_info.address_info)
      } : {}, {
        o: common_vendor.t(detail.value.order_code),
        p: common_vendor.o(($event) => copy(detail.value.order_code)),
        q: common_vendor.t(orderCode.value),
        r: common_vendor.o(($event) => copy(orderCode.value)),
        s: common_vendor.t(detail.value.create_time),
        t: common_vendor.t(detail.value.refund_time || "-"),
        v: common_vendor.t(detail.value.apply_price),
        w: common_vendor.t(detail.value.refund_price),
        x: detail.value.failure_reason
      }, detail.value.failure_reason ? {
        y: common_vendor.t(detail.value.failure_reason)
      } : {}, {
        z: detail.value.refund_text
      }, detail.value.refund_text ? {
        A: common_vendor.t(detail.value.refund_text)
      } : {}) : {}, {
        e: detail.value,
        B: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/refund/apply"))
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-e8e81022"]]);
wx.createPage(MiniProgramPage);
