"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  _easycom_Icon2();
}
const _easycom_Icon = () => "../Icon/Icon.js";
if (!Math) {
  (_easycom_Icon + Popup)();
}
const Popup = () => "../Popup/Popup.js";
const _sfc_main = {
  __name: "Category",
  props: {
    categories: {
      type: Array,
      required: true,
      default: () => []
    },
    height: {
      type: String,
      default: "40vh"
    },
    rightWidth: {
      type: String,
      default: "550rpx"
      // 固定右侧宽度
    }
  },
  emits: ["categoryChange", "subCategoryChange"],
  setup(__props, { expose: __expose, emit: __emit }) {
    const props = __props;
    const isShowMore = common_vendor.ref(false);
    const moreCateList = common_vendor.ref([]);
    const closeMore = () => {
      isShowMore.value = false;
    };
    const openMore = () => {
      var _a;
      isShowMore.value = true;
      moreCateList.value = ((_a = props.categories[activeIndex.value]) == null ? void 0 : _a.subCategories) || [];
    };
    __expose({
      updateActiveIndex(index) {
        activeIndex.value = index;
      }
    });
    const emit = __emit;
    const activeIndex = common_vendor.ref(0);
    const activeSubIndex = common_vendor.ref(0);
    common_vendor.ref(null);
    common_vendor.ref(null);
    const scrollTop = common_vendor.ref(0);
    const scrollLeft = common_vendor.ref(0);
    const currentSubCategories = common_vendor.computed(() => {
      var _a;
      return ((_a = props.categories[activeIndex.value]) == null ? void 0 : _a.subCategories) || [];
    });
    const currentContent = common_vendor.computed(() => {
      var _a;
      return ((_a = props.categories[activeIndex.value]) == null ? void 0 : _a.content) || [];
    });
    const currentDisplayContent = common_vendor.computed(() => {
      var _a;
      const content = currentContent.value;
      const subCategories = currentSubCategories.value;
      if (subCategories.length > 0) {
        const selectedSubId = (_a = subCategories[activeSubIndex.value]) == null ? void 0 : _a.id;
        return content.filter((item) => item.subCategoryId === selectedSubId);
      }
      return content;
    });
    common_vendor.watch(activeIndex, () => {
      activeSubIndex.value = 0;
      scrollTop.value = 0;
      scrollLeft.value = 0;
    });
    common_vendor.watch(activeSubIndex, async (newIndex) => {
      await common_vendor.nextTick$1();
      if (currentSubCategories.value.length > 0) {
        scrollToCenter(newIndex);
      }
    });
    const scrollToCenter = (index) => {
      const query = common_vendor.index.createSelectorQuery();
      query.select("#subNav" + index).boundingClientRect();
      query.select(".sub-nav-scroll").boundingClientRect();
      query.exec((res) => {
        if (res[0] && res[1]) {
          const selectedRect = res[0];
          const scrollViewRect = res[1];
          const targetScrollLeft = selectedRect.left + scrollLeft.value - scrollViewRect.left - scrollViewRect.width / 2 + selectedRect.width / 2;
          scrollLeft.value = Math.max(0, targetScrollLeft);
        }
      });
    };
    const handleNavClick = async (index) => {
      activeIndex.value = index;
      emit("categoryChange", {
        index,
        category: props.categories[index]
      });
      await common_vendor.nextTick$1();
      if (currentSubCategories.value.length > 0) {
        setTimeout(() => {
          scrollToCenter(0);
        }, 50);
      }
    };
    const handleSubNavClick = async (subIndex) => {
      activeSubIndex.value = subIndex;
      scrollTop.value = 0;
      isShowMore.value = false;
      emit("subCategoryChange", {
        mainCategoryIndex: activeIndex.value,
        subCategoryIndex: subIndex,
        subCategory: currentSubCategories.value[subIndex]
      });
      await common_vendor.nextTick$1();
      scrollToCenter(subIndex);
    };
    const handleSubNavScroll = (e) => {
      scrollLeft.value = e.detail.scrollLeft;
    };
    const handleScroll = (e) => {
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(__props.categories, (category, index, i0) => {
          return {
            a: common_vendor.t(category.name),
            b: index,
            c: activeIndex.value === index ? 1 : "",
            d: common_vendor.o(($event) => handleNavClick(index), index)
          };
        }),
        b: currentSubCategories.value.length > 0
      }, currentSubCategories.value.length > 0 ? common_vendor.e({
        c: common_vendor.f(currentSubCategories.value, (subItem, subIndex, i0) => {
          return {
            a: common_vendor.t(subItem.name),
            b: subIndex,
            c: activeSubIndex.value === subIndex ? 1 : "",
            d: "subNav" + subIndex,
            e: common_vendor.o(($event) => handleSubNavClick(subIndex), subIndex)
          };
        }),
        d: currentSubCategories.value.length > 6
      }, currentSubCategories.value.length > 6 ? {
        e: common_vendor.p({
          name: isShowMore.value ? "up" : "down",
          size: "24rpx",
          color: "#e1a038"
        }),
        f: common_vendor.o(openMore)
      } : {}, {
        g: scrollLeft.value,
        h: common_vendor.o(handleSubNavScroll)
      }) : {}, {
        i: common_vendor.f(currentDisplayContent.value, (item, index, i0) => {
          return {
            a: "d-" + i0,
            b: common_vendor.r("d", {
              item,
              index
            }, i0),
            c: index
          };
        }),
        j: currentDisplayContent.value.length === 0
      }, currentDisplayContent.value.length === 0 ? {} : {}, {
        k: scrollTop.value,
        l: common_vendor.o(handleScroll),
        m: __props.rightWidth,
        n: __props.height,
        o: common_vendor.p({
          name: "close",
          size: "30rpx",
          color: "#666"
        }),
        p: common_vendor.o(closeMore),
        q: common_vendor.f(moreCateList.value, (item, index, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: activeSubIndex.value === index ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => handleSubNavClick(index))
          };
        }),
        r: common_vendor.o(($event) => isShowMore.value = $event),
        s: common_vendor.p({
          showTitle: false,
          showButtons: false,
          position: "bottom",
          visible: isShowMore.value
        })
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-c17e5517"]]);
wx.createComponent(Component);
