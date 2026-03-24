"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "Navbar",
  props: {
    needPlaceholder: {
      type: Boolean,
      default: true
    },
    title: {
      type: String,
      default: ""
    },
    backgroundColor: {
      type: String,
      default: "#ffffff"
    },
    color: {
      type: String,
      default: "#000000"
    },
    showBack: {
      type: Boolean,
      default: true
    },
    backText: {
      type: String,
      default: ""
    },
    useDefaultRight: {
      type: Boolean,
      default: false
    },
    rightText: {
      type: String,
      default: "完成"
    },
    immersive: {
      type: Boolean,
      default: false
    },
    // 自定义导航栏内容区高度
    navbarContentHeight: {
      type: Number,
      default: 44
    },
    // 是否需要自动计算并通知外部高度（推荐开启）
    autoCalculateHeight: {
      type: Boolean,
      default: true
    }
  },
  emits: ["left-click", "right-click", "height-change"],
  setup(__props, { expose: __expose, emit: __emit }) {
    const props = __props;
    const emit = __emit;
    const safeAreaTop = common_vendor.ref(0);
    const totalHeight = common_vendor.ref(0);
    common_vendor.ref(null);
    const navbarTotalHeight = common_vendor.computed(() => {
      return safeAreaTop.value + props.navbarContentHeight;
    });
    const navbarStyle = common_vendor.computed(() => {
      return {
        height: navbarTotalHeight.value + "px"
      };
    });
    const bgStyle = common_vendor.computed(() => {
      if (props.immersive) {
        return {
          backgroundColor: "transparent",
          opacity: 0
        };
      }
      return {
        backgroundColor: props.backgroundColor,
        color: props.color
      };
    });
    const handleLeftClick = () => {
      emit("left-click");
      if (props.showBack) {
        const pages = getCurrentPages();
        if (pages.length > 1) {
          common_vendor.index.navigateBack();
        }
      }
    };
    const handleRightClick = () => {
      emit("right-click");
    };
    const getSystemInfo = () => {
      try {
        const systemInfo = common_vendor.index.getSystemInfoSync();
        const menuButtonInfo = common_vendor.index.getMenuButtonBoundingClientRect();
        const statusBarHeight = systemInfo.statusBarHeight || 0;
        safeAreaTop.value = statusBarHeight;
        if (props.autoCalculateHeight) {
          const recommendedHeight = menuButtonInfo.height + (menuButtonInfo.top - statusBarHeight) * 2;
          emit("height-change", {
            safeAreaTop: safeAreaTop.value,
            navbarHeight: recommendedHeight,
            totalHeight: safeAreaTop.value + recommendedHeight
          });
        }
        if (!safeAreaTop.value) {
          safeAreaTop.value = systemInfo.statusBarHeight || 0;
        }
        totalHeight.value = safeAreaTop.value + props.navbarContentHeight;
        if (props.autoCalculateHeight) {
          emit("height-change", {
            safeAreaTop: safeAreaTop.value,
            navbarHeight: props.navbarContentHeight,
            totalHeight: totalHeight.value
          });
        }
      } catch (error) {
        safeAreaTop.value = 44;
        totalHeight.value = safeAreaTop.value + props.navbarContentHeight;
      }
    };
    common_vendor.onMounted(() => {
      getSystemInfo();
    });
    __expose({
      // 获取导航栏总高度
      getNavbarHeight: () => totalHeight.value,
      // 获取安全区域高度
      getSafeAreaTop: () => safeAreaTop.value,
      // 重新计算
      recalculate: getSystemInfo
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: safeAreaTop.value + "px",
        b: common_vendor.s(bgStyle.value),
        c: __props.showBack
      }, __props.showBack ? common_vendor.e({
        d: __props.backText
      }, __props.backText ? {
        e: common_vendor.t(__props.backText)
      } : {}) : {}, {
        f: common_vendor.o(handleLeftClick),
        g: common_vendor.t(__props.title),
        h: __props.useDefaultRight
      }, __props.useDefaultRight ? {
        i: common_vendor.t(__props.rightText),
        j: common_vendor.o(handleRightClick)
      } : {}, {
        k: __props.navbarContentHeight + "px",
        l: safeAreaTop.value + "px",
        m: common_vendor.s(navbarStyle.value),
        n: __props.needPlaceholder
      }, __props.needPlaceholder ? {
        o: navbarTotalHeight.value + "px"
      } : {});
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-c9cb3a3e"]]);
wx.createComponent(Component);
