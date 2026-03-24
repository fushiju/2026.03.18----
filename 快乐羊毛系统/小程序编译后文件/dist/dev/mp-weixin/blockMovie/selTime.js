"use strict";
const common_vendor = require("../common/vendor.js");
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  const _easycom_Price2 = common_vendor.resolveComponent("Price");
  (_easycom_Icon2 + _easycom_Price2)();
}
const _easycom_Icon = () => "../components/Icon/Icon.js";
const _easycom_Price = () => "../components/Price/Price.js";
if (!Math) {
  (_easycom_Icon + _easycom_Price)();
}
const _sfc_main = {
  __name: "selTime",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const current = common_vendor.ref(0);
    const movieView = common_vendor.computed(() => `tab-${current.value}`);
    const movieList = common_vendor.ref([
      {
        id: 1,
        title: "飞驰人生3",
        img: "https://img0.baidu.com/it/u=934468808,1877460626&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=750",
        rating: 9.5,
        wantLook: 1087721,
        director: "韩寒",
        actor: "沈腾，尹正，黄景瑜，沙溢",
        time: 125,
        type: "喜剧,剧情"
      },
      {
        id: 2,
        title: "镖人:风起大漠",
        img: "https://n.sinaimg.cn/sinakd20260124s/742/w594h948/20260124/b014-710a9ec5dc398cbb646c82420aa7ce3f.jpg",
        rating: 9.5,
        wantLook: 1087721,
        director: "韩寒",
        actor: "沈腾，尹正，黄景瑜，沙溢",
        time: 125,
        type: "喜剧,剧情"
      },
      {
        id: 3,
        title: "惊蛰无声",
        img: "https://wx1.sinaimg.cn/mw690/6b8762ccly1i9jaqzykooj20j60qutmd.jpg",
        rating: 9.5,
        wantLook: 1087721,
        director: "韩寒",
        actor: "沈腾，尹正，黄景瑜，沙溢",
        time: 125,
        type: "喜剧,剧情"
      },
      {
        id: 4,
        title: "夜王",
        img: "https://q9.itc.cn/q_70/images01/20260109/6c757c6495f146ada54bd01e22a7f52a.jpeg",
        rating: 9.5,
        wantLook: 1087721,
        director: "韩寒",
        actor: "沈腾，尹正，黄景瑜，沙溢",
        time: 125,
        type: "喜剧,剧情"
      },
      {
        id: 5,
        title: "熊猫计划之部落奇遇记",
        img: "https://inews.gtimg.com/news_bt/OQNuVL5JTyf3peozVOHpMMGEC9-mQk7Qb-l6C-goEGMbEAA/641",
        rating: 9.5,
        wantLook: 1087721,
        director: "韩寒",
        actor: "沈腾，尹正，黄景瑜，沙溢",
        time: 125,
        type: "喜剧,剧情"
      },
      {
        id: 6,
        title: "熊出没之年年有雄",
        img: "https://q8.itc.cn/q_70/images03/20260203/5240710bb7024d6da979fa1439822ad0.jpeg",
        rating: 9.5,
        wantLook: 1087721,
        director: "韩寒",
        actor: "沈腾，尹正，黄景瑜，沙溢",
        time: 125,
        type: "喜剧,剧情"
      }
    ]);
    const selMovie = (index) => {
      current.value = index;
      common_vendor.index.setNavigationBarTitle({
        title: movieList.value[current.value].title
      });
    };
    let anchor = common_vendor.ref(0);
    const tabIntoView = common_vendor.computed(() => `tab-${anchor.value}`);
    const dateList = common_vendor.ref([
      { id: 1, name: "今日3月6日" },
      { id: 2, name: "明日3月7日" },
      { id: 3, name: "后日3月8日" },
      { id: 4, name: "周一3月9日" },
      { id: 5, name: "周二3月10日" },
      { id: 6, name: "周三3月11日" },
      { id: 7, name: "周四3月12日" },
      { id: 8, name: "周五3月13日" },
      { id: 9, name: "周六3月14日" },
      { id: 10, name: "周日3月15日" }
    ]);
    const selTime = (e) => {
      anchor.value = e;
    };
    const timeList = common_vendor.ref([
      {
        id: 1,
        startTime: "13:20",
        endTime: "15:10",
        type: "国语 2D",
        room: "1号厅",
        sale: "41.52",
        oldPrice: "52.80",
        economy: "1.28"
      },
      {
        id: 2,
        startTime: "15:30",
        endTime: "16:20",
        type: "国语 2D",
        room: "6号厅",
        sale: "41.52",
        oldPrice: "52.80",
        economy: "11.28"
      }
    ]);
    common_vendor.onLoad((e) => {
      common_vendor.index.setNavigationBarTitle({
        title: movieList.value[current.value].title
      });
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.p({
          name: "location",
          size: 30,
          color: "#f9be5f"
        }),
        b: common_vendor.f(common_vendor.unref(movieList), (item, index, i0) => {
          return {
            a: common_vendor.unref(current) === index ? 1 : "",
            b: item.img,
            c: index,
            d: common_vendor.o(($event) => selMovie(index), index),
            e: "tab-" + index
          };
        }),
        c: common_vendor.unref(movieView),
        d: common_vendor.t(common_vendor.unref(movieList)[common_vendor.unref(current)].title),
        e: common_vendor.t(common_vendor.unref(movieList)[common_vendor.unref(current)].rating),
        f: common_vendor.t(common_vendor.unref(movieList)[common_vendor.unref(current)].time),
        g: common_vendor.t(common_vendor.unref(movieList)[common_vendor.unref(current)].type),
        h: common_vendor.t(common_vendor.unref(movieList)[common_vendor.unref(current)].actor),
        i: common_vendor.f(common_vendor.unref(dateList), (item, index, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: common_vendor.unref(anchor) === index ? 1 : "",
            c: index,
            d: "tab-" + index,
            e: common_vendor.o(($event) => selTime(index), index)
          };
        }),
        j: common_vendor.unref(tabIntoView),
        k: common_vendor.f(common_vendor.unref(timeList), (item, index, i0) => {
          return {
            a: common_vendor.t(item.startTime),
            b: common_vendor.t(item.endTime),
            c: common_vendor.t(item.type),
            d: common_vendor.t(item.room),
            e: common_vendor.t(item.oldPrice),
            f: "3dd4e0ab-1-" + i0,
            g: common_vendor.p({
              value: item.sale
            }),
            h: common_vendor.t(item.economy),
            i: index,
            j: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/blockMovie/seatSelection?id=${item.id}`), index)
          };
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-3dd4e0ab"]]);
wx.createPage(MiniProgramPage);
