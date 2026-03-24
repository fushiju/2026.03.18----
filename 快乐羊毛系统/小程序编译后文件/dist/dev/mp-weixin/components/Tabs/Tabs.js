"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "Tabs",
  props: {
    // 选项卡数据
    tabs: {
      type: Array,
      default: () => [],
      required: true
    },
    // 当前激活索引
    modelValue: {
      type: Number,
      default: 0
    },
    // 选项卡类型：line（线条型）、card（卡片型）、segment（分段器）
    type: {
      type: String,
      default: "line",
      validator: (val) => ["line", "card", "segment", "button"].includes(val)
    },
    // 是否可滚动
    scrollable: {
      type: Boolean,
      default: false
    },
    // 是否显示指示器
    showIndicator: {
      type: Boolean,
      default: true
    },
    // 是否显示分段器背景
    showSegmentBg: {
      type: Boolean,
      default: true
    },
    // 激活颜色
    activeColor: {
      type: String,
      default: "#007aff"
    },
    // 默认颜色
    inactiveColor: {
      type: String,
      default: "#333333"
    },
    // 指示器颜色
    indicatorColor: {
      type: String,
      default: ""
    },
    // 指示器高度
    indicatorHeight: {
      type: [String, Number],
      default: 4
    },
    // 指示器宽度类型：auto（自适应）、fixed（固定宽度）
    indicatorWidth: {
      type: String,
      default: "auto",
      validator: (val) => ["auto", "fixed"].includes(val)
    },
    // 固定指示器宽度
    fixedIndicatorWidth: {
      type: [String, Number],
      default: 40
    },
    // 指示器圆角
    indicatorRadius: {
      type: [String, Number],
      default: 2
    },
    // 是否等分
    equalWidth: {
      type: Boolean,
      default: false
    },
    // 间距
    gap: {
      type: [String, Number],
      default: 0
    },
    // 字体大小
    fontSize: {
      type: [String, Number],
      default: 24
    },
    // 激活字体粗细
    activeFontWeight: {
      type: [String, Number],
      default: "bold"
    },
    // 默认字体粗细
    inactiveFontWeight: {
      type: [String, Number],
      default: "normal"
    },
    // 背景颜色
    backgroundColor: {
      type: String,
      default: "#ffffff"
    },
    // 高度
    height: {
      type: [String, Number],
      default: 88
    },
    // 是否动画切换
    animated: {
      type: Boolean,
      default: true
    },
    // 动画持续时间（毫秒）
    duration: {
      type: Number,
      default: 300
    },
    // 点击时是否震动
    vibrate: {
      type: Boolean,
      default: false
    },
    // 是否支持手势滑动（需配合父组件实现）
    swipeable: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    "update:modelValue",
    "change",
    "click",
    "disabled-click"
  ],
  setup(__props, { expose: __expose, emit: __emit }) {
    const props = __props;
    const emit = __emit;
    const currentIndex = common_vendor.ref(props.modelValue);
    const scrollLeft = common_vendor.ref(0);
    const containerWidth = common_vendor.ref(0);
    const indicatorInfo = common_vendor.ref({
      left: 0,
      width: 0
    });
    const tabRects = common_vendor.ref([]);
    const tabsStyle = common_vendor.computed(() => {
      const style = {
        backgroundColor: props.backgroundColor,
        height: typeof props.height === "number" ? `${props.height}rpx` : props.height,
        width: "100%"
      };
      return style;
    });
    const segmentBgStyle = common_vendor.computed(() => {
      if (props.type !== "segment")
        return {};
      const activeTab = tabRects.value[currentIndex.value];
      if (!activeTab)
        return {};
      return {
        left: `${activeTab.left}px`,
        width: `${activeTab.width}px`,
        backgroundColor: props.activeColor,
        borderRadius: typeof props.indicatorRadius === "number" ? `${props.indicatorRadius}rpx` : props.indicatorRadius,
        transition: props.animated ? `all ${props.duration}ms ease` : "none"
      };
    });
    const indicatorStyle = common_vendor.computed(() => {
      if (!props.showIndicator || props.type === "segment")
        return {};
      const info = indicatorInfo.value;
      const style = {
        left: `${info.left}px`,
        width: `${info.width}px`,
        backgroundColor: props.indicatorColor || props.activeColor,
        height: typeof props.indicatorHeight === "number" ? `${props.indicatorHeight}rpx` : props.indicatorHeight,
        borderRadius: typeof props.indicatorRadius === "number" ? `${props.indicatorRadius}rpx` : props.indicatorRadius,
        transition: props.animated ? `all ${props.duration}ms ease` : "none"
      };
      if (props.type === "card") {
        style.top = "auto";
        style.bottom = 0;
      }
      return style;
    });
    const formatBadge = (badge) => {
      if (typeof badge === "number") {
        return badge > 99 ? "99+" : badge.toString();
      }
      return badge;
    };
    const getTabItemStyle = (item, index) => {
      const isActive = currentIndex.value === index;
      const style = {};
      if (props.equalWidth && !props.scrollable) {
        style.flex = 1;
      }
      if (props.gap && index > 0) {
        style.marginLeft = typeof props.gap === "number" ? `${props.gap}rpx` : props.gap;
      }
      if (props.fontSize) {
        style.fontSize = typeof props.fontSize === "number" ? `${props.fontSize}rpx` : props.fontSize;
      }
      style.fontWeight = isActive ? props.activeFontWeight : props.inactiveFontWeight;
      if (props.type === "card") {
        if (isActive) {
          style.backgroundColor = props.activeColor;
          style.color = "#ffffff";
        } else {
          style.backgroundColor = "#f5f5f5";
          style.color = props.inactiveColor;
        }
      }
      if (props.type === "segment") {
        if (isActive) {
          style.color = "#ffffff";
        } else {
          style.color = props.inactiveColor;
        }
      }
      if (props.type === "button") {
        if (isActive) {
          style.borderColor = props.activeColor;
          style.color = props.activeColor;
        } else {
          style.borderColor = "#e4e7ed";
          style.color = props.inactiveColor;
        }
      }
      if (props.type === "line" || props.type === "button") {
        style.color = isActive ? props.activeColor : props.inactiveColor;
      }
      if (item.disabled) {
        style.opacity = 0.5;
        style.cursor = "not-allowed";
      }
      return style;
    };
    const handleTabClick = (index, item) => {
      if (item.disabled) {
        emit("disabled-click", { index, item });
        if (props.vibrate)
          ;
        return;
      }
      currentIndex.value = index;
      emit("update:modelValue", index);
      emit("change", { index, item });
      emit("click", { index, item });
      if (props.vibrate)
        ;
      common_vendor.nextTick$1(() => {
        updateIndicatorPosition(index);
        if (props.scrollable) {
          scrollToTab(index);
        }
      });
    };
    const updateIndicatorPosition = (index) => {
      if (!props.showIndicator || props.type === "segment")
        return;
      const tabRect = tabRects.value[index];
      if (!tabRect)
        return;
      let indicatorWidth = 0;
      if (props.indicatorWidth === "fixed") {
        indicatorWidth = typeof props.fixedIndicatorWidth === "number" ? props.fixedIndicatorWidth : parseInt(props.fixedIndicatorWidth);
      } else {
        indicatorWidth = tabRect.width;
      }
      indicatorInfo.value = {
        left: tabRect.left + (tabRect.width - indicatorWidth) / 2,
        width: indicatorWidth
      };
    };
    const scrollToTab = (index) => {
      if (!props.scrollable)
        return;
      const tabRect = tabRects.value[index];
      if (!tabRect)
        return;
      const scrollViewWidth = containerWidth.value;
      const tabCenter = tabRect.left + tabRect.width / 2;
      const scrollLeft2 = Math.max(0, tabCenter - scrollViewWidth / 2);
      scrollLeft2.value = scrollLeft2;
    };
    const getTabRects = () => {
      if (!props.tabs.length)
        return;
      const query = common_vendor.index.createSelectorQuery();
      const selectors = [];
      props.tabs.forEach((_, index) => {
        selectors.push(query.select(`.tab-item:nth-child(${index + 1})`));
      });
      selectors.forEach((selector, index) => {
        selector.boundingClientRect((rect) => {
          if (rect) {
            tabRects.value[index] = {
              left: rect.left,
              width: rect.width,
              height: rect.height
            };
            if (index === 0 && tabRects.value.length === props.tabs.length) {
              updateIndicatorPosition(currentIndex.value);
            }
          }
        }).exec();
      });
    };
    common_vendor.watch(() => props.modelValue, (newVal) => {
      if (newVal !== currentIndex.value) {
        currentIndex.value = newVal;
        common_vendor.nextTick$1(() => {
          updateIndicatorPosition(newVal);
          if (props.scrollable) {
            scrollToTab(newVal);
          }
        });
      }
    });
    common_vendor.watch(() => props.tabs, () => {
      common_vendor.nextTick$1(() => {
        getTabRects();
      });
    }, { deep: true });
    common_vendor.onMounted(() => {
      common_vendor.nextTick$1(() => {
        getTabRects();
        const query = common_vendor.index.createSelectorQuery();
        query.select(".custom-tabs").boundingClientRect((rect) => {
          if (rect) {
            containerWidth.value = rect.width;
          }
        }).exec();
      });
    });
    __expose({
      switchTab: (index) => {
        if (index >= 0 && index < props.tabs.length) {
          handleTabClick(index, props.tabs[index]);
        }
      },
      nextTab: () => {
        const nextIndex = (currentIndex.value + 1) % props.tabs.length;
        handleTabClick(nextIndex, props.tabs[nextIndex]);
      },
      prevTab: () => {
        const prevIndex = currentIndex.value === 0 ? props.tabs.length - 1 : currentIndex.value - 1;
        handleTabClick(prevIndex, props.tabs[prevIndex]);
      }
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: __props.scrollable
      }, __props.scrollable ? common_vendor.e({
        b: __props.type === "segment" && __props.showSegmentBg
      }, __props.type === "segment" && __props.showSegmentBg ? {
        c: common_vendor.s(segmentBgStyle.value)
      } : {}, {
        d: __props.showIndicator && __props.type !== "segment"
      }, __props.showIndicator && __props.type !== "segment" ? {
        e: common_vendor.s(indicatorStyle.value)
      } : {}, {
        f: common_vendor.f(__props.tabs, (item, index, i0) => {
          return common_vendor.e(_ctx.$slots.default ? {
            a: "d-" + i0,
            b: common_vendor.r("d", {
              item,
              index,
              active: currentIndex.value === index
            }, i0)
          } : common_vendor.e({
            c: item.icon || item.iconActive
          }, item.icon || item.iconActive ? common_vendor.e({
            d: item.icon && currentIndex.value !== index
          }, item.icon && currentIndex.value !== index ? {
            e: item.icon
          } : item.iconActive && currentIndex.value === index ? {
            g: item.iconActive
          } : item.iconClass ? {
            i: common_vendor.n(item.iconClass),
            j: common_vendor.n(currentIndex.value === index ? item.iconActiveClass : "")
          } : {}, {
            f: item.iconActive && currentIndex.value === index,
            h: item.iconClass
          }) : {}, {
            k: common_vendor.t(item.title),
            l: currentIndex.value === index ? 1 : "",
            m: item.badge
          }, item.badge ? {
            n: common_vendor.t(formatBadge(item.badge)),
            o: common_vendor.n(item.badgeType || "default")
          } : {}), {
            p: item.key || index,
            q: common_vendor.n({
              "tab-active": currentIndex.value === index,
              "tab-disabled": item.disabled
            }),
            r: common_vendor.s(getTabItemStyle(item, index)),
            s: common_vendor.o(($event) => handleTabClick(index, item), item.key || index)
          });
        }),
        g: _ctx.$slots.default,
        h: common_vendor.n(`tab-${__props.type}`),
        i: scrollLeft.value,
        j: common_vendor.o((...args) => _ctx.onScroll && _ctx.onScroll(...args))
      }) : common_vendor.e({
        k: __props.type === "segment" && __props.showSegmentBg
      }, __props.type === "segment" && __props.showSegmentBg ? {
        l: common_vendor.s(segmentBgStyle.value)
      } : {}, {
        m: __props.showIndicator && __props.type !== "segment"
      }, __props.showIndicator && __props.type !== "segment" ? {
        n: common_vendor.s(indicatorStyle.value)
      } : {}, {
        o: common_vendor.f(__props.tabs, (item, index, i0) => {
          return common_vendor.e(_ctx.$slots.default ? {
            a: "d-" + i0,
            b: common_vendor.r("d", {
              item,
              index,
              active: currentIndex.value === index
            }, i0)
          } : common_vendor.e({
            c: item.icon || item.iconActive
          }, item.icon || item.iconActive ? common_vendor.e({
            d: item.icon && currentIndex.value !== index
          }, item.icon && currentIndex.value !== index ? {
            e: item.icon
          } : item.iconActive && currentIndex.value === index ? {
            g: item.iconActive
          } : item.iconClass ? {
            i: common_vendor.n(item.iconClass),
            j: common_vendor.n(currentIndex.value === index ? item.iconActiveClass : "")
          } : {}, {
            f: item.iconActive && currentIndex.value === index,
            h: item.iconClass
          }) : {}, {
            k: common_vendor.t(item.title),
            l: currentIndex.value === index ? 1 : "",
            m: item.badge
          }, item.badge ? {
            n: common_vendor.t(formatBadge(item.badge)),
            o: common_vendor.n(item.badgeType || "default")
          } : {}), {
            p: item.key || index,
            q: common_vendor.n({
              "tab-active": currentIndex.value === index,
              "tab-disabled": item.disabled
            }),
            r: common_vendor.s(getTabItemStyle(item, index)),
            s: common_vendor.o(($event) => handleTabClick(index, item), item.key || index)
          });
        }),
        p: _ctx.$slots.default,
        q: common_vendor.n(`tab-${__props.type}`),
        r: __props.type !== "segment" ? 1 : ""
      }), {
        s: common_vendor.s(tabsStyle.value)
      });
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-563eb7b4"]]);
wx.createComponent(Component);
