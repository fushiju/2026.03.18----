"use strict";
const common_vendor = require("../../common/vendor.js");
const api_my = require("../../api/my.js");
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const statusMap = {
      1: { text: "待退款", cls: "pending" },
      2: { text: "同意退款", cls: "agree" },
      3: { text: "拒绝退款", cls: "reject" },
      4: { text: "退款中", cls: "processing" },
      5: { text: "退款失败", cls: "failed" }
    };
    const activeTab = common_vendor.ref(0);
    const listData = common_vendor.ref([]);
    const loading = common_vendor.ref(false);
    const refreshing = common_vendor.ref(false);
    const page = common_vendor.ref(1);
    const status = common_vendor.ref("more");
    const formatItem = (item) => {
      var _a, _b;
      const goods = ((_a = item.order_goods) == null ? void 0 : _a[0]) || {};
      const statusInfo = statusMap[item.status] || { text: "未知", cls: "" };
      return {
        id: item.id,
        order_code: item.order_code,
        status_num: item.status,
        status_text: statusInfo.text,
        status_class: statusInfo.cls,
        image: goods.goods_cover || "",
        title: goods.goods_name || "",
        technician: ((_b = item.coach_info) == null ? void 0 : _b.coach_name) || "",
        price: goods.goods_price ?? 0,
        quantity: goods.num ?? 1,
        total: item.have_price ?? 0,
        refund: item.apply_price ?? 0
      };
    };
    const loadList = async (isRefresh = false) => {
      var _a;
      if (loading.value)
        return;
      if (isRefresh) {
        page.value = 1;
        status.value = "more";
      }
      if (status.value === "noMore" && !isRefresh)
        return;
      loading.value = true;
      status.value = "loading";
      try {
        const params = { page: page.value, limit: 10 };
        if (activeTab.value !== 0)
          params.status = activeTab.value;
        const res = await api_my.orderInfo(params);
        const pageData = ((_a = res == null ? void 0 : res.data) == null ? void 0 : _a.data) || [];
        const formatted = pageData.map(formatItem);
        const total = (res == null ? void 0 : res.data.total) || 0;
        if (isRefresh) {
          listData.value = formatted;
        } else {
          listData.value = [...listData.value, ...formatted];
        }
        if (listData.value.length >= total || formatted.length < 10) {
          status.value = "noMore";
        } else {
          status.value = "more";
          page.value++;
        }
      } catch (e) {
        status.value = "more";
      } finally {
        loading.value = false;
      }
    };
    const switchTab = (index) => {
      activeTab.value = index;
      loadList(true);
    };
    const onRefresh = async () => {
      refreshing.value = true;
      await loadList(true);
      refreshing.value = false;
    };
    const onLoadMore = () => {
      if (status.value !== "noMore") {
        loadList();
      }
    };
    const handleGoods = (item) => {
      proxy.$u.goUrl(
        `/subPages/refund/detail?status=${item.status_num}&id=${item.id}`
      );
    };
    common_vendor.onLoad(() => {
      loadList(true);
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: activeTab.value === 0 ? 1 : "",
        b: common_vendor.o(($event) => switchTab(0)),
        c: activeTab.value === 1 ? 1 : "",
        d: common_vendor.o(($event) => switchTab(1)),
        e: activeTab.value === 2 ? 1 : "",
        f: common_vendor.o(($event) => switchTab(2)),
        g: activeTab.value === 3 ? 1 : "",
        h: common_vendor.o(($event) => switchTab(3)),
        i: activeTab.value === 4 ? 1 : "",
        j: common_vendor.o(($event) => switchTab(4)),
        k: activeTab.value === 5 ? 1 : "",
        l: common_vendor.o(($event) => switchTab(5)),
        m: listData.value.length > 0
      }, listData.value.length > 0 ? {
        n: common_vendor.f(listData.value, (item, k0, i0) => {
          return {
            a: common_vendor.t(item.order_code),
            b: common_vendor.t(item.status_text),
            c: common_vendor.n(item.status_class),
            d: item.image,
            e: common_vendor.t(item.title),
            f: common_vendor.t(item.technician),
            g: common_vendor.t(item.price),
            h: common_vendor.t(item.quantity),
            i: common_vendor.t(item.total),
            j: common_vendor.t(item.refund),
            k: item.id,
            l: common_vendor.o(($event) => handleGoods(item), item.id)
          };
        })
      } : !loading.value ? {} : {}, {
        o: !loading.value,
        p: listData.value.length > 0
      }, listData.value.length > 0 ? common_vendor.e({
        q: status.value === "loading"
      }, status.value === "loading" ? {} : {}, {
        r: status.value === "noMore"
      }, status.value === "noMore" ? {} : {}) : {}, {
        s: refreshing.value,
        t: common_vendor.o(onRefresh),
        v: common_vendor.o(onLoadMore)
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-6869c762"]]);
wx.createPage(MiniProgramPage);
