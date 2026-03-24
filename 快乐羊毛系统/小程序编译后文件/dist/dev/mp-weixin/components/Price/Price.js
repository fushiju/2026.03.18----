"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "Price",
  props: {
    // 价格值（必填）
    value: {
      type: [Number, String],
      required: true,
      default: 0
    },
    // 货币符号
    symbol: {
      type: String,
      default: "¥"
    },
    // 是否显示货币符号
    showSymbol: {
      type: Boolean,
      default: true
    },
    // 小数位数
    decimalPlaces: {
      type: Number,
      default: 2,
      validator: (val) => val >= 0 && val <= 4
    },
    // 是否显示小数部分
    showDecimal: {
      type: Boolean,
      default: true
    },
    // 千分位分隔符
    thousandsSeparator: {
      type: Boolean,
      default: true
    },
    // 分隔符字符
    separatorChar: {
      type: String,
      default: ","
    },
    // 单位（如：元、起）
    unit: {
      type: String,
      default: ""
    },
    // 是否显示单位
    showUnit: {
      type: Boolean,
      default: true
    },
    // 原价（划线价）
    originalPrice: {
      type: [Number, String],
      default: null
    },
    // 是否显示原价
    showOriginal: {
      type: Boolean,
      default: false
    },
    // 折扣率（0-1）
    discountRate: {
      type: Number,
      default: 0,
      validator: (val) => val >= 0 && val <= 1
    },
    // 是否显示折扣标签
    showDiscount: {
      type: Boolean,
      default: false
    },
    // 折扣标签文字
    discountText: {
      type: String,
      default: ""
    },
    // 主价格颜色
    color: {
      type: String,
      default: "#ff3b30"
    },
    // 主价格字体大小（单位：rpx）
    size: {
      type: [Number, String],
      default: 36
    },
    // 主价格字体粗细
    fontWeight: {
      type: [Number, String],
      default: "bold"
    },
    // 符号字体大小
    symbolSize: {
      type: [Number, String],
      default: null
    },
    // 符号位置：before（前面）、superscript（上标）
    symbolPosition: {
      type: String,
      default: "before",
      validator: (val) => ["before", "superscript"].includes(val)
    },
    // 小数字体大小
    decimalSize: {
      type: [Number, String],
      default: null
    },
    // 单位字体大小
    unitSize: {
      type: [Number, String],
      default: null
    },
    // 原价颜色
    originalColor: {
      type: String,
      default: "#999999"
    },
    // 原价字体大小
    originalSize: {
      type: [Number, String],
      default: 24
    },
    // 折扣标签背景色
    discountBgColor: {
      type: String,
      default: "#ff3b30"
    },
    // 折扣标签文字颜色
    discountColor: {
      type: String,
      default: "#ffffff"
    },
    // 折扣标签字体大小
    discountSize: {
      type: [Number, String],
      default: 20
    },
    // 是否紧凑显示（去除空格）
    compact: {
      type: Boolean,
      default: false
    },
    // 对齐方式：left, center, right
    align: {
      type: String,
      default: "left",
      validator: (val) => ["left", "center", "right"].includes(val)
    }
  },
  setup(__props) {
    common_vendor.useCssVars((_ctx) => ({
      "51b4179d": props.align,
      "8e57598c": props.discountColor,
      "5efe2a0e": typeof props.discountSize === "number" ? `${props.discountSize}rpx` : props.discountSize
    }));
    const props = __props;
    const formatNumber = (num) => {
      if (num === null || num === void 0 || num === "")
        return "";
      const number = parseFloat(num);
      if (isNaN(number))
        return "";
      const fixedNum = number.toFixed(props.decimalPlaces);
      if (props.thousandsSeparator) {
        const parts = fixedNum.split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, props.separatorChar);
        return parts.join(".");
      }
      return fixedNum;
    };
    const parsedPrice = common_vendor.computed(() => {
      const price = parseFloat(props.value);
      return isNaN(price) ? 0 : price;
    });
    const integerPart = common_vendor.computed(() => {
      const priceStr = formatNumber(parsedPrice.value);
      if (!priceStr)
        return "0";
      const parts = priceStr.split(".");
      return parts[0];
    });
    const decimalPart = common_vendor.computed(() => {
      if (!props.showDecimal || props.decimalPlaces === 0)
        return "";
      const priceStr = parsedPrice.value.toFixed(props.decimalPlaces);
      const parts = priceStr.split(".");
      return parts[1] || "00";
    });
    common_vendor.computed(() => {
      if (props.discountText)
        return props.discountText;
      if (props.discountRate > 0) {
        const discount = Math.round(props.discountRate * 100);
        return `${discount}折`;
      }
      return "";
    });
    const symbolStyle = common_vendor.computed(() => {
      const style = {
        color: props.color,
        fontSize: props.symbolSize ? `${props.symbolSize}rpx` : `${parseInt(props.size) * 0.8}rpx`
      };
      if (props.symbolPosition === "superscript") {
        style.verticalAlign = "super";
        style.fontSize = `${parseInt(props.size) * 0.6}rpx`;
        style.lineHeight = 1;
      }
      return style;
    });
    const integerStyle = common_vendor.computed(() => ({
      color: props.color,
      fontSize: typeof props.size === "number" ? `${props.size}rpx` : props.size,
      fontWeight: props.fontWeight
    }));
    const decimalStyle = common_vendor.computed(() => ({
      color: props.color,
      fontSize: props.decimalSize ? `${props.decimalSize}rpx` : `${parseInt(props.size) * 0.7}rpx`,
      fontWeight: props.fontWeight
    }));
    const unitStyle = common_vendor.computed(() => ({
      color: props.color,
      fontSize: props.unitSize ? `${props.unitSize}rpx` : `${parseInt(props.size) * 0.6}rpx`,
      marginLeft: props.compact ? "0" : "8rpx"
    }));
    const originalStyle = common_vendor.computed(() => ({
      color: props.originalColor,
      fontSize: typeof props.originalSize === "number" ? `${props.originalSize}rpx` : props.originalSize,
      textDecoration: "line-through",
      marginLeft: "16rpx"
    }));
    const discountStyle = common_vendor.computed(() => ({
      backgroundColor: props.discountBgColor,
      borderRadius: "4rpx",
      padding: "4rpx 8rpx",
      marginLeft: "12rpx",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center"
    }));
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: __props.showSymbol
      }, __props.showSymbol ? {
        b: common_vendor.t(__props.symbol),
        c: common_vendor.s(symbolStyle.value)
      } : {}, {
        d: common_vendor.t(integerPart.value),
        e: common_vendor.s(integerStyle.value),
        f: __props.showDecimal && decimalPart.value
      }, __props.showDecimal && decimalPart.value ? {
        g: common_vendor.t(decimalPart.value),
        h: common_vendor.s(decimalStyle.value)
      } : {}, {
        i: __props.showUnit && __props.unit
      }, __props.showUnit && __props.unit ? {
        j: common_vendor.t(__props.unit),
        k: common_vendor.s(unitStyle.value)
      } : {}, {
        l: __props.showOriginal && __props.originalPrice
      }, __props.showOriginal && __props.originalPrice ? {
        m: common_vendor.t(formatNumber(__props.originalPrice)),
        n: common_vendor.s(originalStyle.value)
      } : {}, {
        o: __props.showDiscount && __props.discountRate > 0
      }, __props.showDiscount && __props.discountRate > 0 ? {
        p: common_vendor.t(__props.discountText),
        q: common_vendor.s(discountStyle.value)
      } : {}, {
        r: common_vendor.s(_ctx.__cssVars())
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-fb9211fe"]]);
wx.createComponent(Component);
