"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "BackTop",
  props: {
    // 显示阈值（单位：px）
    threshold: {
      type: Number,
      default: 300
    },
    // 按钮位置
    position: {
      type: String,
      default: "bottom-right",
      validator: (val) => [
        "bottom-right",
        "bottom-left",
        "top-right",
        "top-left"
      ].includes(val)
    },
    // 距离边缘距离
    offset: {
      type: [Number, Object],
      default: () => ({ x: 40, y: 40 })
    },
    // 按钮大小
    size: {
      type: Number,
      default: 80
    },
    // 背景颜色
    backgroundColor: {
      type: String,
      default: "#007aff"
    },
    // 文字颜色
    color: {
      type: String,
      default: "#ffffff"
    },
    // 是否显示文字
    showText: {
      type: Boolean,
      default: false
    },
    // 按钮文字
    buttonText: {
      type: String,
      default: "顶部"
    },
    // 滚动动画时长
    duration: {
      type: Number,
      default: 300
    },
    // 图标
    icon: {
      type: String,
      default: ""
    },
    // 图标URL
    iconUrl: {
      type: String,
      default: ""
    },
    // 图标大小
    iconSize: {
      type: Number,
      default: 36
    },
    // 是否显示阴影
    shadow: {
      type: Boolean,
      default: true
    },
    // 圆角大小
    borderRadius: {
      type: Number,
      default: 50
    },
    // z-index
    zIndex: {
      type: Number,
      default: 9999
    },
    // 强制显示（用于调试）
    forceShow: {
      type: Boolean,
      default: false
    },
    // 初始是否显示
    initialShow: {
      type: Boolean,
      default: false
    },
    // 监听页面滚动（小程序专用）
    listenPageScroll: {
      type: Boolean,
      default: true
    }
  },
  emits: ["click", "show", "hide", "scroll"],
  setup(__props, { expose: __expose, emit: __emit }) {
    const props = __props;
    const emit = __emit;
    const shouldShow = common_vendor.ref(props.initialShow || props.forceShow);
    const showAnimation = common_vendor.ref(false);
    const isTouching = common_vendor.ref(false);
    const currentScrollTop = common_vendor.ref(0);
    common_vendor.ref(0);
    common_vendor.ref(0);
    const initialized = common_vendor.ref(false);
    const buttonStyle = common_vendor.computed(() => {
      const style = {};
      const offsetX = typeof props.offset === "number" ? props.offset : props.offset.x || 40;
      const offsetY = typeof props.offset === "number" ? props.offset : props.offset.y || 40;
      style.width = `${props.size}rpx`;
      style.height = `${props.size}rpx`;
      style.backgroundColor = props.backgroundColor;
      style.color = props.color;
      style.zIndex = props.zIndex;
      style.borderRadius = `${props.borderRadius}%`;
      if (props.shadow) {
        style.boxShadow = "0 4rpx 16rpx rgba(0, 0, 0, 0.2)";
      }
      style.position = "fixed";
      switch (props.position) {
        case "bottom-right":
          style.bottom = `${offsetY}rpx`;
          style.right = `${offsetX}rpx`;
          break;
        case "bottom-left":
          style.bottom = `${offsetY}rpx`;
          style.left = `${offsetX}rpx`;
          break;
        case "top-right":
          style.top = `${offsetY}rpx`;
          style.right = `${offsetX}rpx`;
          break;
        case "top-left":
          style.top = `${offsetY}rpx`;
          style.left = `${offsetX}rpx`;
          break;
      }
      if (isTouching.value) {
        style.transform = "scale(0.95)";
        style.opacity = "0.8";
      }
      return style;
    });
    const scrollToTop = () => {
      emit("click");
      if (typeof common_vendor.index !== "undefined" && common_vendor.index.pageScrollTo) {
        common_vendor.index.pageScrollTo({
          scrollTop: 0,
          duration: props.duration,
          success: () => {
            setTimeout(() => {
              shouldShow.value = false;
              currentScrollTop.value = 0;
            }, props.duration + 100);
          },
          fail: (err) => {
          }
        });
      }
    };
    const onTouchStart = () => {
      isTouching.value = true;
    };
    const onTouchEnd = () => {
      isTouching.value = false;
    };
    const handleScroll = (scrollTop) => {
      currentScrollTop.value = scrollTop;
      emit("scroll", scrollTop);
      const show = scrollTop > props.threshold;
      if (show !== shouldShow.value) {
        shouldShow.value = show;
        if (show) {
          showAnimation.value = true;
          emit("show", scrollTop);
          setTimeout(() => {
            showAnimation.value = false;
          }, 300);
        } else {
          emit("hide", scrollTop);
        }
      }
    };
    __expose({
      show: () => {
        shouldShow.value = true;
        showAnimation.value = true;
      },
      hide: () => {
        shouldShow.value = false;
      },
      toggle: () => {
        shouldShow.value = !shouldShow.value;
      },
      getScrollPosition: () => currentScrollTop.value,
      // 小程序页面滚动回调
      onPageScroll: (e) => {
        if (props.listenPageScroll) {
          handleScroll(e.scrollTop);
        }
      }
    });
    common_vendor.watch(() => props.forceShow, (newVal) => {
      shouldShow.value = newVal;
      if (newVal) {
        showAnimation.value = true;
      }
    });
    common_vendor.onMounted(() => {
      initialized.value = true;
      setTimeout(() => {
      }, 1e3);
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: __props.icon
      }, __props.icon ? {
        b: common_vendor.t(__props.icon)
      } : __props.iconUrl ? {
        d: __props.iconUrl
      } : {}, {
        c: __props.iconUrl,
        e: __props.showText
      }, __props.showText ? {
        f: common_vendor.t(__props.buttonText)
      } : {}, {
        g: shouldShow.value,
        h: common_vendor.n(__props.position),
        i: common_vendor.n({
          "show-animation": showAnimation.value
        }),
        j: common_vendor.s(buttonStyle.value),
        k: common_vendor.o(scrollToTop),
        l: common_vendor.o(onTouchStart),
        m: common_vendor.o(onTouchEnd)
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-6b19d381"]]);
wx.createComponent(Component);
