"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "Popup",
  props: {
    // 是否显示
    visible: {
      type: Boolean,
      default: false
    },
    // 标题
    title: {
      type: String,
      default: "提示"
    },
    // 是否显示标题
    showTitle: {
      type: Boolean,
      default: true
    },
    // 消息内容
    message: {
      type: String,
      default: ""
    },
    // 按钮配置
    buttons: {
      type: Array,
      default: () => [
        { text: "取消", type: "default" },
        { text: "确定", type: "primary" }
      ]
    },
    // 是否显示按钮
    showButtons: {
      type: Boolean,
      default: true
    },
    // 按钮布局：horizontal, vertical
    buttonLayout: {
      type: String,
      default: "horizontal",
      validator: (val) => ["horizontal", "vertical"].includes(val)
    },
    // 是否显示关闭按钮
    showClose: {
      type: Boolean,
      default: true
    },
    // 关闭按钮位置：top-right, top-left
    closePosition: {
      type: String,
      default: "top-right",
      validator: (val) => ["top-right", "top-left"].includes(val)
    },
    // 点击遮罩是否关闭
    maskClosable: {
      type: Boolean,
      default: true
    },
    // 是否显示遮罩
    showMask: {
      type: Boolean,
      default: true
    },
    // 遮罩颜色
    maskColor: {
      type: String,
      default: "rgba(0, 0, 0, 0.5)"
    },
    // 弹框宽度
    width: {
      type: [Number, String],
      default: 600
    },
    // 弹框最大宽度
    maxWidth: {
      type: [Number, String],
      default: "90vw"
    },
    // 弹框位置：center, top, bottom, left, right
    position: {
      type: String,
      default: "center",
      validator: (val) => ["center", "top", "bottom", "left", "right"].includes(val)
    },
    // 动画类型：fade, slide, zoom, none
    animation: {
      type: String,
      default: "fade",
      validator: (val) => ["fade", "slide", "zoom", "none"].includes(val)
    },
    // 动画方向（slide时有效）：top, bottom, left, right
    animationDirection: {
      type: String,
      default: "top",
      validator: (val) => ["top", "bottom", "left", "right"].includes(val)
    },
    // 是否显示圆角
    rounded: {
      type: Boolean,
      default: true
    },
    // 圆角大小
    borderRadius: {
      type: [Number, String],
      default: 16
    },
    // 背景颜色
    backgroundColor: {
      type: String,
      default: "#ffffff"
    },
    // 标题颜色
    titleColor: {
      type: String,
      default: "#333333"
    },
    // 标题大小
    titleSize: {
      type: [Number, String],
      default: 36
    },
    // 消息颜色
    messageColor: {
      type: String,
      default: "#666666"
    },
    // 消息大小
    messageSize: {
      type: [Number, String],
      default: 30
    },
    // 消息对齐方式
    messageAlign: {
      type: String,
      default: "center",
      validator: (val) => ["left", "center", "right"].includes(val)
    },
    // 是否可滚动
    scrollable: {
      type: Boolean,
      default: false
    },
    // 最大高度
    maxHeight: {
      type: [Number, String],
      default: "70vh"
    },
    // 是否全屏
    fullscreen: {
      type: Boolean,
      default: false
    },
    // 是否锁定滚动（阻止页面滚动）
    lockScroll: {
      type: Boolean,
      default: true
    },
    // 是否显示阴影
    showShadow: {
      type: Boolean,
      default: true
    },
    // 自定义类名
    customClass: {
      type: String,
      default: ""
    },
    // 自定义样式
    customStyle: {
      type: Object,
      default: () => ({})
    }
  },
  emits: [
    "update:visible",
    "open",
    "close",
    "confirm",
    "cancel",
    "button-click",
    "mask-click"
  ],
  setup(__props, { expose: __expose, emit: __emit }) {
    common_vendor.useCssVars((_ctx) => ({
      "70db07e0": typeof props.titleSize === "number" ? `${props.titleSize}rpx` : props.titleSize,
      "2f78354a": props.titleColor,
      "66fde1d8": props.scrollable ? "auto" : "visible",
      "0b916df1": typeof props.messageSize === "number" ? `${props.messageSize}rpx` : props.messageSize,
      "7ff0b13b": props.messageColor,
      "7fd318dd": props.messageAlign
    }));
    const props = __props;
    const emit = __emit;
    const internalVisible = common_vendor.ref(props.visible);
    const maskClass = common_vendor.computed(() => {
      const classes = [];
      if (props.showMask) {
        classes.push("mask-visible");
      }
      if (props.animation !== "none") {
        classes.push(`mask-${props.animation}`);
      }
      return classes.join(" ");
    });
    const containerClass = common_vendor.computed(() => {
      const classes = [];
      classes.push(`position-${props.position}`);
      if (props.animation !== "none") {
        classes.push(`animation-${props.animation}`);
        if (props.animation === "slide") {
          classes.push(`slide-from-${props.animationDirection}`);
        }
      }
      classes.push(`close-${props.closePosition}`);
      if (props.rounded) {
        classes.push("rounded");
      }
      if (props.customClass) {
        classes.push(props.customClass);
      }
      return classes.join(" ");
    });
    const maskStyle = common_vendor.computed(() => ({
      backgroundColor: props.showMask ? props.maskColor : "transparent"
    }));
    const containerStyle = common_vendor.computed(() => {
      const style = {
        ...props.customStyle
      };
      if (props.fullscreen) {
        style.width = "100vw";
        style.height = "100vh";
        style.maxWidth = "100vw";
        style.maxHeight = "100vh";
      } else {
        if (props.position === "bottom") {
          style.width = "100%";
          style.maxWidth = "100%";
        } else {
          style.width = typeof props.width === "number" ? `${props.width}rpx` : props.width;
          style.maxWidth = props.maxWidth;
        }
      }
      style.backgroundColor = props.backgroundColor;
      if (props.rounded) {
        style.borderRadius = typeof props.borderRadius === "number" ? `${props.borderRadius}rpx` : props.borderRadius;
      }
      if (props.showShadow && !props.fullscreen) {
        style.boxShadow = "0 20rpx 60rpx rgba(0, 0, 0, 0.2)";
      }
      if (!props.fullscreen && props.maxHeight) {
        style.maxHeight = props.maxHeight;
      }
      return style;
    });
    const computedButtons = common_vendor.computed(() => {
      return props.buttons.map((btn) => ({
        ...btn,
        type: btn.type || "default",
        outline: btn.outline !== void 0 ? btn.outline : false
      }));
    });
    const getButtonStyle = (btn, index) => {
      const style = {};
      if (props.buttonLayout === "horizontal" && index > 0) {
        style.marginLeft = "20rpx";
      }
      if (props.buttonLayout === "vertical" && index > 0) {
        style.marginTop = "20rpx";
      }
      return style;
    };
    const handleMaskClick = () => {
      emit("mask-click");
      if (props.maskClosable) {
        handleClose();
      }
    };
    const handleClose = () => {
      internalVisible.value = false;
      emit("update:visible", false);
      emit("close");
    };
    const handleButtonClick = (btn) => {
      emit("button-click", btn);
      if (btn.handler) {
        btn.handler();
      }
      if (btn.autoClose !== false) {
        handleClose();
      }
      if (btn.type === "primary" || btn.type === "confirm") {
        emit("confirm", btn);
      } else if (btn.type === "default" || btn.type === "cancel") {
        emit("cancel", btn);
      }
    };
    const preventScroll = (prevent) => {
      if (!props.lockScroll)
        return;
      if (prevent) {
        document.body.style.overflow = "hidden";
        document.documentElement.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "";
        document.documentElement.style.overflow = "";
      }
    };
    const show = () => {
      internalVisible.value = true;
      emit("update:visible", true);
      emit("open");
    };
    const hide = () => {
      internalVisible.value = false;
      emit("update:visible", false);
      emit("close");
    };
    common_vendor.watch(() => props.visible, (newVal) => {
      internalVisible.value = newVal;
      if (newVal) {
        emit("open");
      } else {
        emit("close");
      }
    });
    common_vendor.watch(internalVisible, (newVal) => {
      preventScroll(newVal);
    });
    common_vendor.onMounted(() => {
      if (internalVisible.value) {
        preventScroll(true);
      }
    });
    common_vendor.onUnmounted(() => {
      preventScroll(false);
    });
    __expose({
      show,
      hide,
      toggle: () => {
        internalVisible.value = !internalVisible.value;
        emit("update:visible", internalVisible.value);
      }
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: __props.visible
      }, __props.visible ? common_vendor.e({
        b: __props.showTitle
      }, __props.showTitle ? common_vendor.e({
        c: common_vendor.t(__props.title),
        d: __props.showClose
      }, __props.showClose ? {
        e: common_vendor.o(handleClose)
      } : {}) : {}, {
        f: common_vendor.t(__props.message),
        g: __props.showButtons
      }, __props.showButtons ? {
        h: common_vendor.f(computedButtons.value, (btn, index, i0) => {
          return {
            a: common_vendor.t(btn.text),
            b: btn.text || index,
            c: common_vendor.n(`btn-${btn.type || "default"}`),
            d: common_vendor.n({
              "btn-outline": btn.outline
            }),
            e: common_vendor.s(getButtonStyle(btn, index)),
            f: common_vendor.o(($event) => handleButtonClick(btn), btn.text || index)
          };
        }),
        i: common_vendor.n(`buttons-${__props.buttonLayout}`)
      } : {}, {
        j: common_vendor.n(containerClass.value),
        k: common_vendor.s(containerStyle.value),
        l: common_vendor.o(() => {
        }),
        m: common_vendor.n(maskClass.value),
        n: common_vendor.s(maskStyle.value),
        o: common_vendor.s(_ctx.__cssVars()),
        p: common_vendor.o(handleMaskClick)
      }) : {});
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-d4b87936"]]);
wx.createComponent(Component);
