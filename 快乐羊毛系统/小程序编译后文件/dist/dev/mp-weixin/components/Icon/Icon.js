"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "Icon",
  props: {
    // 图标名称（对应iconfont的class名）
    name: {
      type: String,
      default: ""
    },
    // Unicode编码（备用）
    unicode: {
      type: String,
      default: ""
    },
    // 本地图片路径
    src: {
      type: String,
      default: ""
    },
    // 颜色
    color: {
      type: String,
      default: "#333333"
    },
    // 大小（支持rpx, px, rem）
    size: {
      type: [String, Number],
      default: 32
    },
    // 自定义类名
    customClass: {
      type: String,
      default: ""
    },
    // 旋转角度
    rotate: {
      type: [String, Number],
      default: 0
    },
    // 动画
    spin: {
      type: Boolean,
      default: false
    },
    // 点击事件
    clickable: {
      type: Boolean,
      default: false
    },
    // 图片模式（仅图片图标有效）
    mode: {
      type: String,
      default: "widthFix"
    },
    // 字体粗细
    weight: {
      type: [String, Number],
      default: "normal"
    },
    // 是否使用iconfont class方式
    useIconClass: {
      type: Boolean,
      default: true
    },
    // 自定义样式
    customStyle: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ["click"],
  setup(__props, { emit: __emit }) {
    const props = __props;
    const emit = __emit;
    const iconType = common_vendor.computed(() => {
      if (props.src)
        return "image";
      if (props.name || props.unicode)
        return props.useIconClass ? "font" : "text";
      return "font";
    });
    const iconClass = common_vendor.computed(() => {
      if (props.name) {
        return `icon-${props.name}`;
      }
      return "";
    });
    const iconContent = common_vendor.computed(() => {
      if (props.unicode) {
        return String.fromCharCode(parseInt(props.unicode, 16));
      }
      return "";
    });
    const iconSrc = common_vendor.computed(() => {
      if (!props.src)
        return "";
      if (props.src.startsWith("http") || props.src.startsWith("//") || props.src.startsWith("data:")) {
        return props.src;
      }
      if (props.src.startsWith("/")) {
        return props.src;
      }
      return `/static/${props.src}`;
    });
    const iconStyle = common_vendor.computed(() => {
      const style = {
        ...props.customStyle
      };
      style.color = props.color;
      if (props.size) {
        if (typeof props.size === "number") {
          style.fontSize = `${props.size}rpx`;
        } else {
          style.fontSize = props.size;
        }
      }
      if (props.rotate) {
        style.transform = `rotate(${props.rotate}deg)`;
        style.transformOrigin = "center center";
      }
      if (props.spin) {
        style.animation = "icon-spin 1.5s infinite linear";
      }
      if (props.weight) {
        style.fontWeight = props.weight;
      }
      if (props.clickable) {
        style.cursor = "pointer";
      }
      return style;
    });
    const imageStyle = common_vendor.computed(() => {
      const style = {
        ...props.customStyle
      };
      if (props.size) {
        const size = typeof props.size === "number" ? `${props.size}rpx` : props.size;
        style.width = size;
        style.height = "auto";
      }
      if (props.rotate) {
        style.transform = `rotate(${props.rotate}deg)`;
      }
      if (props.clickable) {
        style.cursor = "pointer";
      }
      return style;
    });
    const handleClick = (e) => {
      if (props.clickable) {
        emit("click", e);
      }
    };
    common_vendor.onMounted(() => {
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: iconType.value === "text" && !__props.useIconClass
      }, iconType.value === "text" && !__props.useIconClass ? {
        b: common_vendor.t(iconContent.value),
        c: common_vendor.n(__props.customClass),
        d: common_vendor.s(iconStyle.value),
        e: common_vendor.o(handleClick)
      } : iconType.value === "font" && __props.useIconClass ? {
        g: common_vendor.n(iconClass.value),
        h: common_vendor.n(__props.customClass),
        i: common_vendor.s(iconStyle.value),
        j: common_vendor.o(handleClick)
      } : iconType.value === "image" ? {
        l: common_vendor.n(__props.customClass),
        m: iconSrc.value,
        n: __props.mode,
        o: common_vendor.s(imageStyle.value),
        p: common_vendor.o(handleClick)
      } : {
        q: common_vendor.t(iconContent.value),
        r: common_vendor.n(__props.customClass),
        s: common_vendor.s(iconStyle.value),
        t: common_vendor.o(handleClick)
      }, {
        f: iconType.value === "font" && __props.useIconClass,
        k: iconType.value === "image"
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-3067495b"]]);
wx.createComponent(Component);
