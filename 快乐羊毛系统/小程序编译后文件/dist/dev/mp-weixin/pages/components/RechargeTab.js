"use strict";
const common_vendor = require("../../common/vendor.js");
const api_my = require("../../api/my.js");
const _sfc_main = {
  __name: "RechargeTab",
  setup(__props) {
    const rechargeList = common_vendor.ref([]);
    const startTime = common_vendor.ref(0);
    const endTime = common_vendor.ref(0);
    const startDateStr = common_vendor.ref("");
    const endDateStr = common_vendor.ref("");
    const showFilterPanel = common_vendor.ref(false);
    const filterTitle = common_vendor.ref("本月");
    const initMonthTime = () => {
      const now = /* @__PURE__ */ new Date();
      const year = now.getFullYear();
      const month = now.getMonth();
      const firstDay = new Date(year, month, 1);
      startDateStr.value = formatDateOnly(firstDay);
      startTime.value = Math.floor(firstDay.getTime() / 1e3);
      const lastDay = new Date(year, month + 1, 0);
      lastDay.setHours(23, 59, 59);
      endDateStr.value = formatDateOnly(lastDay);
      endTime.value = Math.floor(lastDay.getTime() / 1e3);
    };
    const formatDateOnly = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      return `${year}-${month}-${day}`;
    };
    const formatDate = (dateStr) => {
      if (!dateStr)
        return "";
      return dateStr;
    };
    const onStartDateChange = (e) => {
      startDateStr.value = e.detail.value;
      const date = new Date(startDateStr.value);
      startTime.value = Math.floor(date.getTime() / 1e3);
    };
    const onEndDateChange = (e) => {
      endDateStr.value = e.detail.value;
      const date = new Date(endDateStr.value);
      date.setHours(23, 59, 59);
      endTime.value = Math.floor(date.getTime() / 1e3);
    };
    const handleCancel = () => {
      showFilterPanel.value = false;
      initMonthTime();
    };
    const handleConfirm = () => {
      showFilterPanel.value = false;
      if (startDateStr.value === endDateStr.value) {
        filterTitle.value = startDateStr.value;
      } else {
        filterTitle.value = `${startDateStr.value} ~ ${endDateStr.value}`;
      }
      rechsrgList();
    };
    const rechsrgList = async () => {
      let params = {
        page: 1,
        start_time: startTime.value,
        end_time: endTime.value
      };
      try {
        const res = await api_my.rechargeRecord(params);
        if (res.data && res.data.data && res.data.data.length > 0) {
          rechargeList.value = res.data.data;
        } else {
          rechargeList.value = [];
        }
      } catch (error) {
      }
    };
    common_vendor.onMounted(() => {
      initMonthTime();
      rechsrgList();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.t(filterTitle.value),
        b: showFilterPanel.value ? 1 : "",
        c: common_vendor.o(($event) => showFilterPanel.value = !showFilterPanel.value),
        d: showFilterPanel.value
      }, showFilterPanel.value ? {
        e: common_vendor.t(startDateStr.value),
        f: startDateStr.value,
        g: common_vendor.o(onStartDateChange),
        h: common_vendor.t(endDateStr.value),
        i: endDateStr.value,
        j: common_vendor.o(onEndDateChange),
        k: common_vendor.o(handleCancel),
        l: common_vendor.o(handleConfirm)
      } : {}, {
        m: rechargeList.value.length > 0
      }, rechargeList.value.length > 0 ? {
        n: common_vendor.f(rechargeList.value, (item, k0, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.t(item.pay_price),
            c: common_vendor.t(formatDate(item.create_time)),
            d: common_vendor.t(item.now_balance),
            e: item.id
          };
        })
      } : {});
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-73b1df77"]]);
wx.createComponent(Component);
