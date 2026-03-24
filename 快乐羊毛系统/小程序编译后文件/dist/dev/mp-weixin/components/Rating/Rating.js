"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Math) {
  Icon();
}
const Icon = () => "../Icon/Icon.js";
const _sfc_main = {
  __name: "Rating",
  props: {
    modelValue: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 5
    },
    readonly: {
      type: Boolean,
      default: false
    },
    showScore: {
      type: Boolean,
      default: true
    },
    activeColor: {
      type: String,
      default: "#ff9800"
    },
    inactiveColor: {
      type: String,
      default: "#ccc"
    },
    allowHalf: {
      type: Boolean,
      default: false
    },
    activeIcon: {
      type: String,
      default: "star-filled"
    },
    inactiveIcon: {
      type: String,
      default: "star-outline"
    },
    iconSize: {
      type: String,
      default: "40rpx"
    }
  },
  emits: ["update:modelValue", "change"],
  setup(__props, { emit: __emit }) {
    const props = __props;
    const emit = __emit;
    const RatingResult = common_vendor.computed(() => {
      return (e) => {
        switch (e) {
          case 1:
            return "不满意";
          case 2:
            return "一般";
          case 3:
            return "满意";
          case 4:
            return "很满意";
          case 5:
            return "非常满意";
          default:
            return "";
        }
      };
    });
    const stars = common_vendor.computed(() => {
      const result = [];
      for (let i = 1; i <= props.max; i++) {
        result.push({ id: i, value: i, isHalf: false });
      }
      return result;
    });
    const getIconName = (star) => {
      return star.value <= props.modelValue ? props.activeIcon : props.inactiveIcon;
    };
    const getIconColor = (star) => {
      return star.value <= props.modelValue ? props.activeColor : props.inactiveColor;
    };
    const handleRate = (value) => {
      if (props.readonly)
        return;
      emit("update:modelValue", value);
      emit("change", value);
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(stars.value, (star, k0, i0) => {
          return {
            a: "2fad325c-0-" + i0,
            b: common_vendor.p({
              name: getIconName(star),
              size: __props.iconSize,
              color: getIconColor(star)
            }),
            c: star.id,
            d: star.value <= __props.modelValue ? 1 : "",
            e: star.isHalf ? 1 : "",
            f: common_vendor.o(($event) => handleRate(star.value), star.id)
          };
        }),
        b: __props.readonly ? 1 : "",
        c: __props.showScore
      }, __props.showScore ? {
        d: common_vendor.t(RatingResult.value(__props.modelValue))
      } : {});
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-2fad325c"]]);
wx.createComponent(Component);
