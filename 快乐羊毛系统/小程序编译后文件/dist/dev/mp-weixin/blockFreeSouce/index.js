"use strict";
const common_vendor = require("../common/vendor.js");
const api_link = require("../api/link.js");
if (!Math) {
  (SwiperCategory + Category)();
}
const SwiperCategory = () => "../components/SwiperCategory/SwiperCategory.js";
const Category = () => "../components/Category/Category.js";
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const iconList = common_vendor.ref([]);
    let initCate = common_vendor.ref(0);
    const categoryRef = common_vendor.ref(null);
    let oneId = common_vendor.ref(0);
    let twoId = common_vendor.ref(0);
    let threeId = common_vendor.ref(0);
    const onIconClick = async (data) => {
      var _a;
      initCate.value = data.item.id;
      oneId.value = data.item.id;
      const currentCategory = iconList.value.find((i) => i.id === initCate.value);
      const children = (currentCategory == null ? void 0 : currentCategory.children) || [];
      const goodsId = getGoodsId(children) ?? oneId.value;
      initLink(goodsId);
      let temp = children.length > 0 ? children : [{
        id: (currentCategory == null ? void 0 : currentCategory.id) || oneId.value,
        name: "全部",
        category_name: "全部",
        pid: (currentCategory == null ? void 0 : currentCategory.id) || oneId.value,
        children: []
      }];
      categoryData.value = temp.map((i) => ({
        ...i,
        name: i.category_name,
        subCategories: (i.children || []).map((sub) => ({
          ...sub,
          name: sub.category_name
          // 确保子分类名称正确赋值
        })),
        content: []
      }));
      (_a = categoryRef.value) == null ? void 0 : _a.updateActiveIndex(0);
    };
    const getLink = async (url) => {
      const autograph = common_vendor.index.getStorageSync("autograph");
      if (!autograph) {
        common_vendor.index.showToast({
          title: "请先登录",
          icon: "none",
          duration: 1500
        });
        setTimeout(() => {
          common_vendor.index.navigateTo({
            url: "/subPages/login"
          });
        }, 1500);
        return;
      }
      common_vendor.index.navigateTo({
        url: `/subPages/webview?url=${encodeURIComponent(url)}`
      });
    };
    const initPage = async (id) => {
      var _a, _b, _c, _d, _e;
      try {
        let res = await api_link.categroy();
        let temp = res.data.filter((i) => i.id === Number(id));
        if (!temp[0] || !temp[0].children) {
          return;
        }
        iconList.value = temp[0].children;
        initCate.value = iconList.value[0].id;
        iconList.value = iconList.value.map((i) => ({
          ...i,
          name: i.category_name,
          icon: i.category_img,
          // 如果没有 children，创建虚拟的"全部"分类
          children: !i.children || i.children.length === 0 ? [{
            id: i.id,
            name: "全部",
            category_name: "全部",
            pid: i.id,
            children: []
          }] : i.children
        }));
        categoryData.value = iconList.value[0].children.map((item) => ({
          ...item,
          name: item.category_name,
          subCategories: item.children || [],
          content: []
        }));
        twoId.value = (_a = categoryData.value[0]) == null ? void 0 : _a.id;
        threeId.value = ((_d = (_c = (_b = categoryData.value[0]) == null ? void 0 : _b.subCategories) == null ? void 0 : _c[0]) == null ? void 0 : _d.id) || twoId.value;
        (_e = categoryRef.value) == null ? void 0 : _e.updateActiveIndex(0);
        initLink(threeId.value);
      } catch (error) {
      }
    };
    const initLink = async (goodsId) => {
      var _a;
      try {
        let result = await api_link.goodsList({ categoryId: goodsId });
        if (!result.data || !Array.isArray(result.data)) {
          categoryData.value = categoryData.value.map((item) => ({
            ...item,
            content: []
          }));
          return;
        }
        const mappedLinks = result.data.filter((it) => it.link_info).map((it) => ({
          // 修改：使用 categoryId 作为匹配键，而不是 link_info.goods_id
          subCategoryId: goodsId,
          title: it.goods_name,
          desc: it.desc || "",
          url: it.link_info.link_url,
          img: it.goods_img
        }));
        const linksBySubCategory = mappedLinks.reduce((acc, link) => {
          const key = link.subCategoryId;
          if (!acc[key]) {
            acc[key] = [];
          }
          acc[key].push(link);
          return acc;
        }, {});
        const updatedCategoryData = ((_a = categoryData.value) == null ? void 0 : _a.map((category) => {
          let content = [];
          if (Array.isArray(category.subCategories) && category.subCategories.length > 0) {
            category.subCategories.forEach((sub) => {
              const links = linksBySubCategory[sub.id] || [];
              content = [...content, ...links];
            });
          } else {
            content = mappedLinks;
          }
          return {
            ...category,
            content
          };
        })) || [];
        categoryData.value = updatedCategoryData;
      } catch (error) {
        categoryData.value = categoryData.value.map((item) => ({
          ...item,
          content: []
        }));
      }
    };
    const curId = common_vendor.ref(0);
    common_vendor.onLoad((e) => {
      curId.value = e.id;
      initPage(curId.value);
    });
    const categoryData = common_vendor.ref([]);
    const getGoodsId = (categoryData2) => {
      const firstChild = categoryData2[0];
      if (firstChild && firstChild.children && firstChild.children.length > 0) {
        return firstChild.children[0].id;
      } else if (firstChild) {
        return firstChild.id;
      } else {
        return void 0;
      }
    };
    const onCategoryChange = (data) => {
      var _a, _b;
      twoId.value = data.category.id;
      if (data.category.name === "全部") {
        const currentChildren = ((_a = iconList.value.find((i) => i.id === initCate.value)) == null ? void 0 : _a.children) || [];
        const firstChildId = ((_b = currentChildren[0]) == null ? void 0 : _b.id) ?? initCate.value;
        initLink(firstChildId);
      } else {
        const goodsId = getGoodsId(data.category.children || []);
        if (goodsId !== void 0) {
          initLink(goodsId);
        } else {
          initLink(twoId.value);
        }
      }
    };
    const onSubCategoryChange = (data) => {
      threeId.value = data.subCategory.id;
      const goodsId = getGoodsId(data.subCategory.children || []);
      if (goodsId !== void 0) {
        initLink(goodsId);
      } else {
        initLink(threeId.value);
      }
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(onIconClick),
        b: common_vendor.p({
          rows: 2,
          cols: 5,
          iconList: iconList.value,
          height: "24.5vh",
          sel: common_vendor.unref(initCate)
        }),
        c: common_vendor.w(({
          item,
          index
        }, s0, i0) => {
          return {
            a: item.img,
            b: common_vendor.t(item.title),
            c: common_vendor.t(item.desc),
            d: common_vendor.o(($event) => getLink(item.url)),
            e: i0,
            f: s0
          };
        }, {
          name: "d",
          path: "c",
          vueId: "37046ec8-1"
        }),
        d: common_vendor.sr(categoryRef, "37046ec8-1", {
          "k": "categoryRef"
        }),
        e: common_vendor.o(onCategoryChange),
        f: common_vendor.o(onSubCategoryChange),
        g: common_vendor.p({
          categories: categoryData.value,
          height: "69vh",
          rightWidth: "600rpx"
        })
      };
    };
  }
};
wx.createPage(_sfc_main);
