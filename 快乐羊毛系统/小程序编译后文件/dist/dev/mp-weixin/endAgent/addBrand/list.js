"use strict";
const common_vendor = require("../../common/vendor.js");
const api_endAgent = require("../../api/endAgent.js");
if (!Array) {
  const _component_uni_search_bar = common_vendor.resolveComponent("uni-search-bar");
  const _component_uni_popup = common_vendor.resolveComponent("uni-popup");
  (_component_uni_search_bar + _component_uni_popup)();
}
const limit = 10;
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const activeIndex = common_vendor.ref(0);
    const search = common_vendor.ref("");
    const brandListData = common_vendor.ref([]);
    const loading = common_vendor.ref(false);
    const noMore = common_vendor.ref(false);
    const page = common_vendor.ref(1);
    let searchTimer = null;
    const isRefreshing = common_vendor.ref(false);
    const approvalPopup = common_vendor.ref(null);
    const approvalData = common_vendor.ref({
      id: null,
      status: 2,
      // 2=通过，4=驳回
      sh_text: ""
    });
    common_vendor.ref([
      { text: "通过", value: 2 },
      { text: "驳回", value: 4 }
    ]);
    const orderStatus = common_vendor.ref([
      { title: "全部", value: 0 },
      { title: "审核中", value: 1 },
      { title: "已授权", value: 2 },
      { title: "已驳回", value: 4 }
    ]);
    const statusText = (status) => {
      const map = { 0: "全部", 1: "审核中", 2: "已授权", 4: "已驳回" };
      return map[status] || "未知";
    };
    const statusColor = (status) => {
      const map = { 1: "#f9a825", 2: "#4caf50", 4: "#ea4e4e" };
      return map[status] || "#333";
    };
    const handleTabClick = (index) => {
      activeIndex.value = index;
      page.value = 1;
      noMore.value = false;
      brandListData.value = [];
      brandList();
    };
    const handleSearch = () => {
      if (searchTimer) {
        clearTimeout(searchTimer);
      }
      searchTimer = setTimeout(() => {
        page.value = 1;
        noMore.value = false;
        brandListData.value = [];
        brandList();
      }, 300);
    };
    const showRejectReason = (item) => {
      approvalData.value.id = item.id;
      approvalData.value.sh_text = item.sh_text || "暂无驳回原因";
      approvalPopup.value.open();
    };
    const closeApprovalModal = () => {
      approvalPopup.value.close();
    };
    const editBrand = (item) => {
      common_vendor.index.navigateTo({ url: `/endAgent/addBrand/add?id=${item.id}` });
    };
    const handleView = (item) => {
      common_vendor.index.navigateTo({ url: `/endAgent/addBrand/add?id=${item.id}&view=1` });
    };
    const brandList = async (isLoadMore = false) => {
      var _a;
      if (loading.value)
        return;
      loading.value = true;
      try {
        const currentStatus = orderStatus.value[activeIndex.value].value;
        const params = {
          page: page.value,
          limit,
          name: search.value || ""
        };
        if (currentStatus !== 0) {
          params.status = currentStatus;
        }
        const res = await api_endAgent.agentBrandList(params);
        console.log("品牌列表：", res);
        const rawList = ((_a = res.data) == null ? void 0 : _a.data) || [];
        const list = Array.isArray(rawList) ? rawList.filter((item) => item != null) : [];
        if (isLoadMore) {
          brandListData.value = [...brandListData.value, ...list];
        } else {
          brandListData.value = list;
        }
        if (list.length < limit) {
          noMore.value = true;
        }
      } catch (e) {
        console.error("品牌列表加载失败:", e);
      } finally {
        loading.value = false;
      }
    };
    common_vendor.onMounted(() => {
      brandList();
    });
    common_vendor.onShow(() => {
      page.value = 1;
      noMore.value = false;
      brandListData.value = [];
      brandList();
    });
    const onPullingDown = async () => {
      if (loading.value)
        return;
      isRefreshing.value = true;
      page.value = 1;
      noMore.value = false;
      brandListData.value = [];
      try {
        await brandList();
      } finally {
        isRefreshing.value = false;
      }
    };
    const onScrollToLower = () => {
      if (noMore.value || loading.value)
        return;
      page.value++;
      brandList(true);
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(handleSearch),
        b: common_vendor.o(($event) => search.value = $event),
        c: common_vendor.p({
          placeholder: "搜索品牌",
          clearButton: "auto",
          cancelButton: "none",
          modelValue: search.value
        }),
        d: common_vendor.o(($event) => common_vendor.index.navigateTo({
          url: "/endAgent/addBrand/add"
        })),
        e: common_vendor.f(orderStatus.value, (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: activeIndex.value === index ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => handleTabClick(index), index)
          };
        }),
        f: !loading.value && brandListData.value.length === 0
      }, !loading.value && brandListData.value.length === 0 ? {} : {}, {
        g: common_vendor.f(brandListData.value, (item, k0, i0) => {
          return common_vendor.e({
            a: common_vendor.t(statusText(item.status)),
            b: statusColor(item.status),
            c: item.work_img || "",
            d: common_vendor.t(item.coach_name),
            e: common_vendor.t(item.id),
            f: common_vendor.t(item.text || "暂无"),
            g: common_vendor.t(item.create_time),
            h: item.status === 4
          }, item.status === 4 ? {
            i: common_vendor.o(($event) => showRejectReason(item), item == null ? void 0 : item.id)
          } : item.status === 1 ? {
            k: common_vendor.o(($event) => editBrand(item), item == null ? void 0 : item.id)
          } : {}, {
            j: item.status === 1,
            l: item == null ? void 0 : item.id,
            m: common_vendor.o(($event) => handleView(item), item == null ? void 0 : item.id)
          });
        }),
        h: brandListData.value.length > 0
      }, brandListData.value.length > 0 ? common_vendor.e({
        i: loading.value
      }, loading.value ? {} : noMore.value ? {} : {}, {
        j: noMore.value
      }) : {}, {
        k: common_vendor.o(onPullingDown),
        l: common_vendor.o(onScrollToLower),
        m: isRefreshing.value,
        n: common_vendor.t(approvalData.value.sh_text),
        o: common_vendor.o(closeApprovalModal),
        p: common_vendor.sr(approvalPopup, "8a694938-1", {
          "k": "approvalPopup"
        }),
        q: common_vendor.p({
          type: "center",
          ["background-color"]: "#fff"
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-8a694938"]]);
wx.createPage(MiniProgramPage);
