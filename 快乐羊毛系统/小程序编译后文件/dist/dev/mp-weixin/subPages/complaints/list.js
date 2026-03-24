"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const activeIndex = common_vendor.ref(0);
    const typeList = common_vendor.ref([
      {
        title: "全部反馈",
        value: 0
      },
      {
        title: "未处理",
        value: 1
      },
      {
        title: "已处理",
        value: 2
      }
    ]);
    const onTabClick = (index) => {
      activeIndex.value = index;
    };
    common_vendor.onLoad(() => {
      initData();
    });
    const list = common_vendor.ref([]);
    const initData = async () => {
      const params = {
        status: activeIndex.value,
        page: 1,
        limit: 10
      };
      let res = await api_common.feedbackList(params);
      if (res.code === 200)
        list.value = res.data.data;
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(common_vendor.unref(typeList), (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.unref(activeIndex) === index ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => onTabClick(index), index)
          };
        }),
        b: common_vendor.f(common_vendor.unref(list), (item, index, i0) => {
          return {
            a: common_vendor.t(item.order_code),
            b: common_vendor.t(item.status == 1 ? "未处理" : "已处理"),
            c: common_vendor.t(item.content),
            d: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/complaints/detail?id=${item.id}`), index),
            e: common_vendor.t(item.type_name),
            f: index
          };
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-f047b7dc"]]);
wx.createPage(MiniProgramPage);
