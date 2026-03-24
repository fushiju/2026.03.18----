"use strict";
const common_vendor = require("../common/vendor.js");
const Navbar = () => "../components/NavBar/Navbar.js";
const _sfc_main = {
  components: { Navbar },
  data() {
    return {
      componentHeight: "calc(100vh - 100px)",
      // 状态图映射：1是可选，0是已售
      statusMap: { available: 1, sold: 0, empty: -1 }
    };
  },
  onLoad() {
    common_vendor.index.getSystemInfo({
      success: (res) => {
        const navHeight = res.statusBarHeight + 44;
        this.componentHeight = `calc(100vh - ${navHeight}px)`;
      }
    });
  },
  onReady() {
    setTimeout(() => {
      this.initSeatMap();
    }, 500);
  },
  methods: {
    initSeatMap() {
      const seatComp = this.$refs.anilSeatRef;
      if (seatComp) {
        const finalData = this.generateLargeSeats();
        if (typeof seatComp.initData === "function") {
          seatComp.initData(finalData);
        } else if (seatComp.$vm && typeof seatComp.$vm.initData === "function") {
          seatComp.$vm.initData(finalData);
        }
      }
    },
    generateLargeSeats() {
      const flattened = [];
      for (let r = 1; r <= 10; r++) {
        for (let c = 1; c <= 12; c++) {
          if (c === 4 || c === 9)
            continue;
          flattened.push({
            YCoord: String(r),
            XCoord: String(c),
            SeatCode: `R${r}C${c}`,
            Status: 1,
            // 1 为可选
            RowNum: String(r),
            ColumnNum: String(c),
            SeatName: `${r}排${c}座`,
            Price: "38"
          });
        }
      }
      return flattened;
    },
    handleConfirm(data) {
      common_vendor.index.$emit("finishSelect", data);
      common_vendor.index.navigateTo({
        url: "/blockMovie/myOrder"
      });
    },
    goBack() {
      common_vendor.index.navigateBack();
    }
  }
};
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  const _component_Navbar = common_vendor.resolveComponent("Navbar");
  const _easycom_anil_seat2 = common_vendor.resolveComponent("anil-seat");
  (_easycom_Icon2 + _component_Navbar + _easycom_anil_seat2)();
}
const _easycom_Icon = () => "../components/Icon/Icon.js";
const _easycom_anil_seat = () => "../uni_modules/anil-seat/components/anil-seat/anil-seat.js";
if (!Math) {
  (_easycom_Icon + _easycom_anil_seat)();
}
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return {
    a: common_vendor.p({
      name: "left",
      size: 46,
      color: "#fff"
    }),
    b: common_vendor.o((...args) => $options.goBack && $options.goBack(...args)),
    c: common_vendor.sr("anilSeatRef", "30c121e5-2"),
    d: common_vendor.o($options.handleConfirm),
    e: common_vendor.p({
      title: "飞驰人生3",
      info: "2025年03月05日 国语 2D 喜剧",
      ["room-name"]: "5号厅",
      max: 6,
      height: $data.componentHeight
    })
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-30c121e5"]]);
wx.createPage(MiniProgramPage);
