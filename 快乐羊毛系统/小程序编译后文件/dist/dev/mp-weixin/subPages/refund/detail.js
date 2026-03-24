"use strict";
const common_vendor = require("../../common/vendor.js");
const api_my = require("../../api/my.js");
const _sfc_main = {
  __name: "detail",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const countdown = common_vendor.ref("00:00:00");
    let timer = null;
    const loading = common_vendor.ref(false);
    const detail = common_vendor.ref(null);
    const orderCode = common_vendor.ref("");
    const statusMap = {
      1: { label: "待退款", color: "#ff9800", desc: "您的退款申请正在等待商家处理" },
      2: { label: "同意退款", color: "#4caf50", desc: "商家已同意退款，款项将原路退回" },
      3: { label: "拒绝退款", color: "#f44336", desc: "商家拒绝了您的退款申请" },
      4: { label: "退款中", color: "#2196f3", desc: "退款正在处理中，请耐心等待" },
      5: { label: "退款失败", color: "#9e9e9e", desc: "退款处理失败，请联系客服" }
    };
    const currentStatus = common_vendor.ref(1);
    const statusInfo = common_vendor.computed(() => statusMap[currentStatus.value] || statusMap[1]);
    const getDetail = async (id) => {
      var _a;
      loading.value = true;
      try {
        const res = await api_my.orderDetail({ id });
        if (res) {
          detail.value = res.data;
          if (res.data.status) {
            currentStatus.value = Number(res.data.status);
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
    const handlLx = () => {
      common_vendor.index.showModal({
        title: "联系平台客服",
        content: "客服电话：400-000-0000",
        confirmText: "立即拨打",
        cancelText: "取消",
        success: ({ confirm }) => {
          if (confirm) {
            common_vendor.index.makePhoneCall({
              phoneNumber: "4000000000",
              fail: () => {
                common_vendor.index.showToast({ title: "拨打失败，请手动拨打", icon: "none" });
              }
            });
          }
        }
      });
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
    const handleCancel = () => {
      common_vendor.index.showModal({
        title: "提示",
        content: "确认要取消这笔退款申请吗？",
        confirmText: "确认取消",
        confirmColor: "#f44336",
        success: async ({ confirm }) => {
          if (!confirm)
            return;
          try {
            common_vendor.index.showLoading({ title: "处理中..." });
            const res = await api_my.cancelRefundOrder({ id: detail.value.id });
            common_vendor.index.hideLoading();
            if (res !== null && res !== void 0) {
              common_vendor.index.showToast({ title: "取消退款成功", icon: "success" });
              await getDetail(detail.value.id);
            } else {
              common_vendor.index.showToast({ title: "取消失败，请重试", icon: "none" });
            }
          } catch (e) {
            common_vendor.index.hideLoading();
            common_vendor.index.showToast({ title: "取消失败，请重试", icon: "none" });
          }
        }
      });
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
      if (options.status) {
        currentStatus.value = Number(options.status);
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
        B: detail.value && detail.value.status == 1
      }, detail.value && detail.value.status == 1 ? {
        C: common_vendor.o(handleCancel)
      } : {}, {
        D: detail.value && [3, 5].includes(detail.value.status)
      }, detail.value && [3, 5].includes(detail.value.status) ? {
        E: common_vendor.o(handlLx)
      } : {}, {
        F: detail.value && detail.value.status == 2
      }, detail.value && detail.value.status == 2 ? {
        G: common_vendor.t(detail.value.refund_price)
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-e495fe53"]]);
wx.createPage(MiniProgramPage);
