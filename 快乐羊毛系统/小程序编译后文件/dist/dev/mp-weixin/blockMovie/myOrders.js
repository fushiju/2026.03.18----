"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  __name: "myOrders",
  setup(__props) {
    const orderList = common_vendor.ref([]);
    const loading = common_vendor.ref(false);
    const isFinished = common_vendor.ref(false);
    let page = 1;
    const fetchOrders = (pageNo) => {
      return new Promise((resolve) => {
        setTimeout(() => {
          if (pageNo > 3) {
            resolve([]);
            return;
          }
          const newData = Array.from({ length: 5 }).map((_, i) => ({
            id: pageNo * 10 + i,
            cinemaName: "保利万和影城（仁安店）",
            status: pageNo === 1 && i === 0 ? "待支付" : "已完成",
            movieName: "飞驰人生3",
            poster: "https://gw.alicdn.com/tfscom/i3/O1CN01Xvruhi1D64s28eMod_!!6000000000166-0-alipicbeacon.jpg_800x800.jpg",
            time: "今天 2026-03-07 12:05:00",
            hallName: "2号厅（激光放映，3小时免费停车）",
            price: "88.00"
          }));
          resolve(newData);
        }, 1e3);
      });
    };
    const loadData = async (reset = false) => {
      if (loading.value)
        return;
      if (reset) {
        page = 1;
        isFinished.value = false;
      }
      loading.value = true;
      const res = await fetchOrders(page);
      loading.value = false;
      if (res.data.length === 0) {
        isFinished.value = true;
      } else {
        if (reset) {
          orderList.value = res.data;
        } else {
          orderList.value = [...orderList.value, ...res.data];
        }
        page++;
      }
      if (reset)
        common_vendor.index.stopPullDownRefresh();
    };
    common_vendor.onPullDownRefresh(() => {
      loadData(true);
    });
    common_vendor.onReachBottom(() => {
      if (!isFinished.value) {
        loadData();
      }
    });
    common_vendor.onMounted(() => {
      loadData(true);
    });
    const onDetail = () => {
      common_vendor.index.navigateTo({
        url: "/blockMovie/orderDetail"
      });
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: orderList.value.length > 0
      }, orderList.value.length > 0 ? {
        b: common_vendor.f(orderList.value, (item, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(item.cinemaName),
            b: common_vendor.t(item.status),
            c: item.status === "已取消" ? 1 : "",
            d: item.poster,
            e: common_vendor.t(item.movieName),
            f: common_vendor.t(item.time),
            g: common_vendor.t(item.hallName),
            h: common_vendor.t(item.price),
            i: item.status === "待支付"
          }, item.status === "待支付" ? {} : {}, {
            j: item.status === "待支付"
          }, item.status === "待支付" ? {} : {}, {
            k: index,
            l: common_vendor.o(onDetail, index)
          });
        }),
        c: common_vendor.t(loading.value ? "正在加载..." : isFinished.value ? "没有更多订单了" : "上拉加载更多")
      } : !loading.value ? {} : {}, {
        d: !loading.value
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-7f5281b4"]]);
wx.createPage(MiniProgramPage);
