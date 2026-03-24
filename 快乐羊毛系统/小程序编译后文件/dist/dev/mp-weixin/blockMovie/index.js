"use strict";
const common_vendor = require("../common/vendor.js");
if (!Math) {
  (Icon + Navbar)();
}
const Navbar = () => "../components/NavBar/Navbar.js";
const Icon = () => "../components/Icon/Icon.js";
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const city = common_vendor.ref("重庆");
    common_vendor.onShow(() => {
      const cityData = common_vendor.index.getStorageSync("city");
      if (cityData && cityData.name) {
        city.value = cityData.name;
      }
    });
    const backUrl = () => {
      common_vendor.index.navigateBack();
    };
    const hotMovieList = common_vendor.ref([
      {
        id: 1,
        title: "飞驰人生3",
        img: "https://img0.baidu.com/it/u=934468808,1877460626&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=750"
      },
      {
        id: 2,
        title: "镖人:风起大漠",
        img: "https://n.sinaimg.cn/sinakd20260124s/742/w594h948/20260124/b014-710a9ec5dc398cbb646c82420aa7ce3f.jpg"
      },
      {
        id: 3,
        title: "惊蛰无声",
        img: "https://wx1.sinaimg.cn/mw690/6b8762ccly1i9jaqzykooj20j60qutmd.jpg"
      },
      {
        id: 4,
        title: "夜王",
        img: "https://q9.itc.cn/q_70/images01/20260109/6c757c6495f146ada54bd01e22a7f52a.jpeg"
      },
      {
        id: 5,
        title: "熊猫计划之部落奇遇记",
        img: "https://inews.gtimg.com/news_bt/OQNuVL5JTyf3peozVOHpMMGEC9-mQk7Qb-l6C-goEGMbEAA/641"
      },
      {
        id: 6,
        title: "熊出没之年年有雄",
        img: "https://q8.itc.cn/q_70/images03/20260203/5240710bb7024d6da979fa1439822ad0.jpeg"
      }
    ]);
    const waitMovieList = common_vendor.ref([
      {
        id: 1,
        title: "飞驰人生3",
        img: "https://img0.baidu.com/it/u=934468808,1877460626&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=750"
      },
      {
        id: 2,
        title: "镖人:风起大漠",
        img: "https://n.sinaimg.cn/sinakd20260124s/742/w594h948/20260124/b014-710a9ec5dc398cbb646c82420aa7ce3f.jpg"
      },
      {
        id: 3,
        title: "惊蛰无声",
        img: "https://wx1.sinaimg.cn/mw690/6b8762ccly1i9jaqzykooj20j60qutmd.jpg"
      },
      {
        id: 4,
        title: "夜王",
        img: "https://q9.itc.cn/q_70/images01/20260109/6c757c6495f146ada54bd01e22a7f52a.jpeg"
      },
      {
        id: 5,
        title: "熊猫计划之部落奇遇记",
        img: "https://inews.gtimg.com/news_bt/OQNuVL5JTyf3peozVOHpMMGEC9-mQk7Qb-l6C-goEGMbEAA/641"
      },
      {
        id: 6,
        title: "熊出没之年年有雄",
        img: "https://q8.itc.cn/q_70/images03/20260203/5240710bb7024d6da979fa1439822ad0.jpeg"
      }
    ]);
    common_vendor.ref([
      {
        id: 1,
        name: "test影院",
        addr: "重庆市渝北区测试街道测试路203号",
        distance: 300
      }
    ]);
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(backUrl),
        b: common_vendor.p({
          name: "left",
          size: 56,
          color: "#333"
        }),
        c: common_vendor.t(common_vendor.unref(city)),
        d: common_vendor.p({
          name: "down",
          size: 22,
          color: "#333"
        }),
        e: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/selCity")),
        f: common_vendor.p({
          name: "search",
          size: 30,
          color: "#999"
        }),
        g: common_vendor.p({
          name: "right",
          size: 22,
          color: "#999"
        }),
        h: common_vendor.f(common_vendor.unref(hotMovieList), (item, index, i0) => {
          return {
            a: item.img,
            b: common_vendor.t(item.title),
            c: index,
            d: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/blockMovie/selCinema?id=${item.id}`), index)
          };
        }),
        i: common_vendor.p({
          name: "right",
          size: 22,
          color: "#999"
        }),
        j: common_vendor.f(common_vendor.unref(waitMovieList), (item, index, i0) => {
          return {
            a: item.img,
            b: common_vendor.t(item.title),
            c: index
          };
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-bb3fa654"]]);
wx.createPage(MiniProgramPage);
