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
  __name: "selCinema",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const districtList = common_vendor.ref([
      {
        id: 0,
        name: "全部"
      },
      {
        id: 1,
        name: "渝北区"
      },
      {
        id: 2,
        name: "渝中区"
      },
      {
        id: 3,
        name: "巴南区"
      },
      {
        id: 4,
        name: "长寿区"
      },
      {
        id: 5,
        name: "沙坪坝区"
      },
      {
        id: 6,
        name: "南岸区"
      },
      {
        id: 7,
        name: "九龙坡"
      },
      {
        id: 8,
        name: "江北区"
      },
      {
        id: 9,
        name: "北碚"
      },
      {
        id: 10,
        name: "綦江区"
      },
      {
        id: 11,
        name: "大渡口"
      },
      {
        id: 12,
        name: "渝北区"
      },
      {
        id: 13,
        name: "万盛"
      },
      {
        id: 14,
        name: "沙坪坝"
      }
    ]);
    const index = common_vendor.ref(0);
    const searchCinema = common_vendor.ref("");
    const isOpenSearch = common_vendor.ref(false);
    const openSearch = () => {
      isOpenSearch.value = true;
    };
    const closeSearch = () => {
      isOpenSearch.value = false;
    };
    const isSelDistrict = common_vendor.ref(false);
    const selDistrict = () => {
      isSelDistrict.value = true;
    };
    const bindPickerChange = (e) => {
      index.value = e.detail.value;
      isSelDistrict.value = false;
    };
    const city = common_vendor.ref("重庆");
    common_vendor.onShow(() => {
      const cityData = common_vendor.index.getStorageSync("city");
      if (cityData && cityData.name) {
        city.value = cityData.name;
      }
    });
    common_vendor.onLoad((e) => {
      common_vendor.index.setNavigationBarTitle({
        title: movieList.value[current.value].title
      });
    });
    const current = common_vendor.ref(0);
    const handleChange = (e) => {
      current.value = e.detail.current;
      common_vendor.index.setNavigationBarTitle({
        title: movieList.value[current.value].title
      });
    };
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
    const timeList = common_vendor.ref([
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
    let anchor = common_vendor.ref(0);
    const tabIntoView = common_vendor.computed(() => `tab-${anchor.value}`);
    const selTime = (e) => {
      anchor.value = e;
    };
    const cinemaList = common_vendor.ref([
      {
        id: 1,
        name: "test影院",
        addr: "重庆市渝北区测试街道测试路203号",
        distance: 300,
        startPrice: 30.12
      }
    ]);
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(common_vendor.unref(movieList), (item, index2, i0) => {
          return {
            a: item.img,
            b: common_vendor.t(item.title),
            c: common_vendor.t(item.rating),
            d: common_vendor.t(item.wantLook),
            e: common_vendor.t(item.director),
            f: common_vendor.t(item.actor),
            g: common_vendor.t(item.time),
            h: common_vendor.t(item.type),
            i: `url(${item.img})`,
            j: index2
          };
        }),
        b: common_vendor.o(handleChange),
        c: common_vendor.unref(current),
        d: common_vendor.f(common_vendor.unref(timeList), (item, index2, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: common_vendor.unref(anchor) === index2 ? 1 : "",
            c: index2,
            d: "tab-" + index2,
            e: common_vendor.o(($event) => selTime(index2), index2)
          };
        }),
        e: common_vendor.unref(tabIntoView),
        f: common_vendor.t(common_vendor.unref(city)),
        g: common_vendor.p({
          name: "down",
          size: 24,
          color: "#999"
        }),
        h: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/selCity")),
        i: common_vendor.t(common_vendor.unref(districtList)[common_vendor.unref(index)].name),
        j: common_vendor.p({
          name: common_vendor.unref(isSelDistrict) ? "up" : "down",
          size: 24,
          color: "#999"
        }),
        k: common_vendor.o(selDistrict),
        l: common_vendor.o(bindPickerChange),
        m: common_vendor.unref(index),
        n: common_vendor.unref(districtList),
        o: common_vendor.unref(isOpenSearch)
      }, common_vendor.unref(isOpenSearch) ? {
        p: common_vendor.unref(searchCinema),
        q: common_vendor.o(($event) => common_vendor.isRef(searchCinema) ? searchCinema.value = $event.detail.value : null),
        r: common_vendor.o(closeSearch)
      } : {
        s: common_vendor.p({
          name: "search",
          size: 30,
          color: "#999"
        }),
        t: common_vendor.o(openSearch)
      }, {
        v: common_vendor.f(common_vendor.unref(cinemaList), (item, index2, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: "3a02fc60-3-" + i0,
            c: common_vendor.p({
              value: item.startPrice
            }),
            d: common_vendor.t(item.addr),
            e: common_vendor.t(item.distance),
            f: index2,
            g: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/blockMovie/selTime?id=${item.id}`), index2)
          };
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-3a02fc60"]]);
wx.createPage(MiniProgramPage);
