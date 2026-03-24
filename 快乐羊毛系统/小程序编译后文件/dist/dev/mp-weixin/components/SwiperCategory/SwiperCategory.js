"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "SwiperCategory",
  props: {
    iconList: {
      type: Array,
      required: true,
      default: () => []
    },
    rows: {
      type: Number,
      default: 2
      // 默认行数
    },
    cols: {
      type: Number,
      default: 4
      // 默认列数
    },
    height: {
      type: String,
      default: "40vh"
      // 默认列数
    },
    sel: {
      type: Number,
      default: 0
    }
  },
  emits: ["iconClick"],
  setup(__props, { emit: __emit }) {
    common_vendor.useCssVars((_ctx) => ({
      "835a1be0": __props.cols
    }));
    const props = __props;
    const emit = __emit;
    const currentPage = common_vendor.ref(0);
    const pageSize = common_vendor.computed(() => props.rows * props.cols);
    const totalPages = common_vendor.computed(() => Math.ceil(props.iconList.length / pageSize.value));
    const paginatedIcons = common_vendor.computed(() => {
      const pages = [];
      for (let i = 0; i < props.iconList.length; i += pageSize.value) {
        pages.push(props.iconList.slice(i, i + pageSize.value));
      }
      return pages;
    });
    const onSwiperChange = (e) => {
      currentPage.value = e.detail.current;
    };
    const handleIconClick = (item, index) => {
      emit("iconClick", { item, index });
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(paginatedIcons.value, (page, pageIndex, i0) => {
          return {
            a: common_vendor.f(page, (item, index, i1) => {
              return {
                a: item.icon,
                b: common_vendor.t(item.name),
                c: item.id === __props.sel ? 1 : "",
                d: index,
                e: common_vendor.o(($event) => handleIconClick(item, pageIndex * __props.rows * __props.cols + index), index)
              };
            }),
            b: pageIndex
          };
        }),
        b: common_vendor.o(onSwiperChange),
        c: totalPages.value > 1
      }, totalPages.value > 1 ? {
        d: common_vendor.f(totalPages.value, (dot, index, i0) => {
          return {
            a: index,
            b: currentPage.value === index ? 1 : ""
          };
        })
      } : {}, {
        e: common_vendor.s({
          height: __props.height
        }),
        f: common_vendor.s(_ctx.__cssVars())
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-946d2e8c"]]);
wx.createComponent(Component);
