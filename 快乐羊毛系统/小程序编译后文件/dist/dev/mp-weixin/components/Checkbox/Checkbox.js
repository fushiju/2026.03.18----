"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "Checkbox",
  props: {
    // 选中状态
    modelValue: {
      type: Boolean,
      default: false
    },
    // 标签文本
    label: {
      type: String,
      default: ""
    },
    // 描述文本
    description: {
      type: String,
      default: ""
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    // 是否只读
    readonly: {
      type: Boolean,
      default: false
    },
    // 是否必填
    required: {
      type: Boolean,
      default: false
    },
    // 是否显示必填标记
    showRequiredMark: {
      type: Boolean,
      default: true
    },
    // 是否无效状态
    invalid: {
      type: Boolean,
      default: false
    },
    // 尺寸大小：small, medium, large
    size: {
      type: String,
      default: "medium",
      validator: (val) => ["small", "medium", "large"].includes(val)
    },
    // 类型：default, square, circle, switch
    type: {
      type: String,
      default: "default",
      validator: (val) => ["default", "square", "circle", "switch"].includes(val)
    },
    // 选中颜色
    checkedColor: {
      type: String,
      default: "#007aff"
    },
    // 未选中颜色
    uncheckedColor: {
      type: String,
      default: "#dcdfe6"
    },
    // 禁用颜色
    disabledColor: {
      type: String,
      default: "#f2f3f5"
    },
    // 文字颜色
    labelColor: {
      type: String,
      default: "#333333"
    },
    // 禁用文字颜色
    disabledLabelColor: {
      type: String,
      default: "#c8c9cc"
    },
    // 描述文字颜色
    descriptionColor: {
      type: String,
      default: "#666666"
    },
    // 文字大小
    labelSize: {
      type: [Number, String],
      default: null
    },
    // 是否显示边框
    showBorder: {
      type: Boolean,
      default: true
    },
    // 边框圆角
    borderRadius: {
      type: [Number, String],
      default: null
    },
    // 是否显示动画效果
    animated: {
      type: Boolean,
      default: true
    },
    // 是否显示点击效果
    showActiveEffect: {
      type: Boolean,
      default: true
    },
    // 自定义值
    value: {
      type: [String, Number, Boolean, Object],
      default: null
    },
    // 是否中间状态（indeterminate）
    indeterminate: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    "update:modelValue",
    "change",
    "click"
  ],
  setup(__props, { expose: __expose, emit: __emit }) {
    common_vendor.useCssVars((_ctx) => ({
      "cac9cc7e": props.borderRadius ? `${props.borderRadius}rpx` : "8rpx",
      "e1e39836": props.uncheckedColor,
      "f0a29268": props.checkedColor,
      "a8511512": props.disabledColor,
      "7aaf95a4": props.showBorder ? "2rpx" : "0"
    }));
    const props = __props;
    const emit = __emit;
    const isChecked = common_vendor.ref(props.modelValue);
    const isTouching = common_vendor.ref(false);
    const isIndeterminate = common_vendor.ref(props.indeterminate);
    const checkboxStyle = common_vendor.computed(() => {
      const style = {};
      if (props.type === "switch") {
        style.display = "flex";
        style.alignItems = "center";
        style.justifyContent = "space-between";
      }
      if (isTouching.value && props.showActiveEffect) {
        style.opacity = 0.7;
      }
      return style;
    });
    common_vendor.computed(() => {
      if (props.type === "switch") {
        return {
          order: 2
          // 开关类型将复选框放在右边
        };
      }
      return {};
    });
    const labelStyle = common_vendor.computed(() => {
      const style = {};
      if (props.disabled) {
        style.color = props.disabledLabelColor;
      } else {
        style.color = props.labelColor;
      }
      if (props.labelSize) {
        style.fontSize = typeof props.labelSize === "number" ? `${props.labelSize}rpx` : props.labelSize;
      } else {
        switch (props.size) {
          case "small":
            style.fontSize = "26rpx";
            break;
          case "medium":
            style.fontSize = "28rpx";
            break;
          case "large":
            style.fontSize = "32rpx";
            break;
        }
      }
      if (props.type === "switch") {
        style.flex = 1;
        style.marginRight = "24rpx";
      } else {
        style.marginLeft = "20rpx";
      }
      return style;
    });
    const descriptionStyle = common_vendor.computed(() => ({
      color: props.descriptionColor,
      fontSize: "24rpx",
      display: "block",
      marginTop: "8rpx",
      marginLeft: props.type === "switch" ? "0" : "60rpx"
    }));
    const handleClick = (event) => {
      if (props.disabled || props.readonly) {
        emit("click", {
          checked: isChecked.value,
          disabled: props.disabled,
          readonly: props.readonly,
          event
        });
        return;
      }
      const newValue = !isChecked.value;
      isChecked.value = newValue;
      if (isIndeterminate.value && newValue) {
        isIndeterminate.value = false;
      }
      emit("update:modelValue", newValue);
      emit("change", {
        checked: newValue,
        value: props.value,
        event
      });
      emit("click", {
        checked: newValue,
        disabled: props.disabled,
        readonly: props.readonly,
        event
      });
    };
    const onTouchStart = () => {
      if (!props.disabled && !props.readonly && props.showActiveEffect) {
        isTouching.value = true;
      }
    };
    const onTouchEnd = () => {
      isTouching.value = false;
    };
    const setIndeterminate = (value) => {
      isIndeterminate.value = value;
    };
    const setChecked = (value) => {
      isChecked.value = value;
      emit("update:modelValue", value);
    };
    common_vendor.watch(() => props.modelValue, (newVal) => {
      isChecked.value = newVal;
    });
    common_vendor.watch(() => props.indeterminate, (newVal) => {
      isIndeterminate.value = newVal;
    });
    __expose({
      toggle: () => handleClick(),
      setChecked,
      setIndeterminate,
      getChecked: () => isChecked.value,
      getIndeterminate: () => isIndeterminate.value
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: isChecked.value
      }, isChecked.value ? {
        b: common_vendor.r("icon", {
          checked: isChecked.value,
          disabled: __props.disabled
        })
      } : {}, {
        c: __props.label || _ctx.$slots.default
      }, __props.label || _ctx.$slots.default ? {
        d: common_vendor.t(__props.label),
        e: common_vendor.s(labelStyle.value),
        f: common_vendor.o(($event) => !__props.disabled && !__props.readonly && handleClick())
      } : {}, {
        g: __props.description
      }, __props.description ? {
        h: common_vendor.t(__props.description),
        i: common_vendor.s(descriptionStyle.value)
      } : {}, {
        j: __props.required && !isChecked.value && __props.showRequiredMark
      }, __props.required && !isChecked.value && __props.showRequiredMark ? {} : {}, {
        k: common_vendor.n(`checkbox-${__props.size}`),
        l: common_vendor.n(`checkbox-${__props.type}`),
        m: common_vendor.n({
          "checkbox-checked": isChecked.value,
          "checkbox-disabled": __props.disabled,
          "checkbox-readonly": __props.readonly,
          "checkbox-invalid": __props.invalid
        }),
        n: common_vendor.s(checkboxStyle.value),
        o: common_vendor.s(_ctx.__cssVars()),
        p: common_vendor.o(handleClick),
        q: common_vendor.o(onTouchStart),
        r: common_vendor.o(onTouchEnd)
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-18939422"]]);
wx.createComponent(Component);
