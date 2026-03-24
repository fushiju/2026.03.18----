"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Math) {
  (Icon + Navbar + ShopRow + ShopBlock + BackTop)();
}
const BackTop = () => "../../components/BackTop/BackTop.js";
const Navbar = () => "../../components/NavBar/Navbar.js";
const Icon = () => "../../components/Icon/Icon.js";
const ShopBlock = () => "../../components/SearchShopItem/SearchShopBlock.js";
const ShopRow = () => "../../components/SearchShopItem/SearchShopRow.js";
const _sfc_main = {
  __name: "searchResult",
  setup(__props) {
    const filterResult = common_vendor.ref({
      keyword: "",
      // 搜索关键词
      brand: {
        // 品牌选择
        index: 0
        // 当前选中的品牌索引
      },
      filters: {
        // 排序筛选
        type: "comprehensive",
        // comprehensive | sales | price
        priceOrder: null
        // null | asc | desc
      },
      tags: {
        // 各品牌下的标签选择
        byBrand: {}
        // key为brandIndex，value为选中的标签数组
      },
      childBrands: [],
      // 子品牌选择
      appliedFilters: []
      // 已应用的所有筛选条件（用于显示）
    });
    const brandChange = (index) => {
      filterResult.value.brand.index = index;
      filterResult.value.brand.name = brandList.value[index].name;
      isShowChildBrand.value = false;
    };
    const toggleTag = (tag, brandIdx) => {
      if (tag === "品牌") {
        isShowChildBrand.value = !isShowChildBrand.value;
      } else {
        if (!filterResult.value.tags.byBrand[brandIdx]) {
          filterResult.value.tags.byBrand[brandIdx] = [];
        }
        const brandTags = filterResult.value.tags.byBrand[brandIdx];
        const index = brandTags.indexOf(tag);
        if (index > -1) {
          brandTags.splice(index, 1);
        } else {
          brandTags.push(tag);
        }
        isShowChildBrand.value = false;
      }
      updateAppliedFilters();
    };
    const isTagSelected = (tag, brandIdx) => {
      if (!filterResult.value.tags.byBrand[brandIdx]) {
        return false;
      }
      return filterResult.value.tags.byBrand[brandIdx].includes(tag);
    };
    const toggleChildBrand = (brand) => {
      const index = filterResult.value.childBrands.indexOf(brand);
      if (index > -1) {
        filterResult.value.childBrands.splice(index, 1);
      } else {
        filterResult.value.childBrands.push(brand);
      }
      updateAppliedFilters();
    };
    const isBrandSelected = (brand) => {
      return filterResult.value.childBrands.includes(brand);
    };
    const updateAppliedFilters = () => {
      const applied = [];
      const currentBrandTags = filterResult.value.tags.byBrand[filterResult.value.brand.index] || [];
      currentBrandTags.forEach((tag) => {
        applied.push({ type: "tag", value: tag, label: tag });
      });
      filterResult.value.childBrands.forEach((brand) => {
        applied.push({ type: "childBrand", value: brand, label: brand });
      });
      if (filterResult.value.filters.type === "sales") {
        applied.push({ type: "filter", value: "sales", label: "销量" });
      } else if (filterResult.value.filters.type === "price") {
        const orderLabel = filterResult.value.filters.priceOrder === "asc" ? "升序" : filterResult.value.filters.priceOrder === "desc" ? "降序" : "";
        applied.push({ type: "filter", value: "price", label: `券后价${orderLabel ? "(" + orderLabel + ")" : ""}` });
      }
      filterResult.value.appliedFilters = applied;
    };
    const resetAllSelection = () => {
      filterResult.value.tags.byBrand[filterResult.value.brand.index] = [];
      filterResult.value.childBrands = [];
      updateAppliedFilters();
    };
    const confirmSelection = () => {
      isShowChildBrand.value = false;
      updateAppliedFilters();
    };
    common_vendor.onLoad((e) => {
      searchKeyword.value = decodeURIComponent(e.keyword);
      filterResult.value.keyword = searchKeyword.value;
    });
    const brandList = common_vendor.ref([
      {
        name: "全网比价",
        icon: "https://wx3.sinaimg.cn/mw690/48374be4gy1huo590nw62j20zo0oeabq.jpg"
      },
      {
        name: "淘宝天猫",
        icon: "https://wx3.sinaimg.cn/mw690/48374be4gy1huo590nw62j20zo0oeabq.jpg",
        tag: ["历史低价", "优惠券", "天猫", "包邮"]
      },
      {
        name: "京东",
        icon: "https://wx3.sinaimg.cn/mw690/48374be4gy1huo590nw62j20zo0oeabq.jpg",
        tag: ["历史低价", "品牌", "优惠券", "京东自营", "京东物流"],
        childBrand: ["test1", "test2", "test3"]
      },
      {
        name: "抖音商城",
        icon: "https://wx3.sinaimg.cn/mw690/48374be4gy1huo590nw62j20zo0oeabq.jpg"
      },
      {
        name: "唯品会",
        icon: "https://wx3.sinaimg.cn/mw690/48374be4gy1huo590nw62j20zo0oeabq.jpg",
        tag: ["历史低价", "唯品自营"]
      },
      {
        name: "拼多多",
        icon: "https://wx3.sinaimg.cn/mw690/48374be4gy1huo590nw62j20zo0oeabq.jpg",
        tag: ["优惠券", "百亿补贴"]
      }
    ]);
    let isShowChildBrand = common_vendor.ref(false);
    const selectFilter = (filterType) => {
      if (filterResult.value.filters.type === filterType && filterType !== "price") {
        return;
      }
      filterResult.value.filters.type = filterType;
      if (filterType === "price") {
        switchPriceSort();
      } else {
        filterResult.value.filters.priceOrder = null;
      }
      isShowChildBrand.value = false;
      updateAppliedFilters();
    };
    const selectPriceSort = () => {
      filterResult.value.filters.type = "price";
      isShowChildBrand.value = false;
      switchPriceSort();
    };
    const switchPriceSort = () => {
      if (filterResult.value.filters.priceOrder === null) {
        filterResult.value.filters.priceOrder = "asc";
      } else if (filterResult.value.filters.priceOrder === "asc") {
        filterResult.value.filters.priceOrder = "desc";
      } else {
        filterResult.value.filters.priceOrder = null;
      }
      updateAppliedFilters();
    };
    const searchKeyword = common_vendor.ref("");
    const searchSuggestions = common_vendor.ref([]);
    const handleInput = () => {
      if (searchKeyword.value.trim()) {
        const baseSuggestions = [
          searchKeyword.value + "手机",
          searchKeyword.value + "电脑",
          searchKeyword.value + "配件"
        ];
        searchSuggestions.value = baseSuggestions.map((suggestion) => ({
          text: suggestion,
          highlightedHtml: highlightTextForDisplay(suggestion, searchKeyword.value)
        }));
      } else {
        searchSuggestions.value = [];
      }
    };
    const highlightTextForDisplay = (text, keyword) => {
      if (!keyword || !text)
        return { text, parts: [{ text, isHighlighted: false }] };
      const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      const regex = new RegExp(`(${escapedKeyword})`, "gi");
      const parts = [];
      let lastIndex = 0;
      let match;
      while ((match = regex.exec(text)) !== null) {
        if (match.index > lastIndex) {
          parts.push({
            text: text.substring(lastIndex, match.index),
            isHighlighted: false
          });
        }
        parts.push({
          text: match[0],
          isHighlighted: true
        });
        lastIndex = regex.lastIndex;
      }
      if (lastIndex < text.length) {
        parts.push({
          text: text.substring(lastIndex),
          isHighlighted: false
        });
      }
      return { text, parts };
    };
    const handleSearch = () => {
      if (!searchKeyword.value.trim())
        return;
      filterResult.value.keyword = searchKeyword.value;
      addToHistory(searchKeyword.value);
      goToSearchResult(searchKeyword.value);
    };
    const selectSuggestion = (keyword) => {
      searchKeyword.value = keyword;
      filterResult.value.keyword = keyword;
      addToHistory(keyword);
      goToSearchResult(keyword);
    };
    const showSearchContent = common_vendor.ref(false);
    const goToSearchResult = (keyword) => {
      searchKeyword.value = keyword;
      searchSuggestions.value = [];
      showSearchContent.value = false;
    };
    const addToHistory = (keyword) => {
      let history = getSearchHistory();
      const index = history.indexOf(keyword);
      if (index !== -1) {
        history.splice(index, 1);
      }
      history.unshift(keyword);
      if (history.length > 10) {
        history.pop();
      }
      saveSearchHistory(history);
    };
    const saveSearchHistory = (history) => {
      try {
        common_vendor.index.setStorageSync("searchHistory", history);
      } catch (e) {
      }
    };
    const getSearchHistory = () => {
      try {
        const history = common_vendor.index.getStorageSync("searchHistory");
        return history ? history : [];
      } catch (e) {
        return [];
      }
    };
    const backUrl = () => {
      common_vendor.index.navigateBack();
    };
    const clearKeyword = () => {
      common_vendor.index.navigateBack();
    };
    return (_ctx, _cache) => {
      var _a, _b;
      return common_vendor.e({
        a: common_vendor.o(backUrl),
        b: common_vendor.p({
          name: "left",
          size: 36,
          color: "#333"
        }),
        c: common_vendor.o(handleSearch),
        d: common_vendor.o([($event) => common_vendor.isRef(searchKeyword) ? searchKeyword.value = $event.detail.value : null, handleInput]),
        e: common_vendor.o(clearKeyword),
        f: common_vendor.unref(searchKeyword),
        g: common_vendor.p({
          fixed: true,
          ["safe-area-inset-top"]: true
        }),
        h: common_vendor.unref(searchKeyword) && common_vendor.unref(searchSuggestions).length > 0
      }, common_vendor.unref(searchKeyword) && common_vendor.unref(searchSuggestions).length > 0 ? {
        i: common_vendor.f(common_vendor.unref(searchSuggestions), (item, index, i0) => {
          return {
            a: common_vendor.f(item.highlightedHtml.parts, (part, partIndex, i1) => {
              return {
                a: common_vendor.t(part.text),
                b: partIndex,
                c: part.isHighlighted ? "#fa6400" : "#333"
              };
            }),
            b: index,
            c: common_vendor.o(($event) => selectSuggestion(item.text), index)
          };
        })
      } : {}, {
        j: common_vendor.f(common_vendor.unref(brandList), (item, index, i0) => {
          return {
            a: item.icon,
            b: common_vendor.t(item.name),
            c: common_vendor.o(($event) => brandChange(index), index),
            d: common_vendor.n({
              "act": index === common_vendor.unref(filterResult).brand.index
            }),
            e: index
          };
        }),
        k: common_vendor.unref(filterResult).brand.index
      }, common_vendor.unref(filterResult).brand.index ? {
        l: common_vendor.unref(filterResult).filters.type === "comprehensive" ? 1 : "",
        m: common_vendor.o(($event) => selectFilter("comprehensive")),
        n: common_vendor.unref(filterResult).filters.type === "sales" ? 1 : "",
        o: common_vendor.o(($event) => selectFilter("sales")),
        p: common_vendor.unref(filterResult).filters.priceOrder === "asc" ? 1 : "",
        q: common_vendor.unref(filterResult).filters.priceOrder === "desc" ? 1 : "",
        r: common_vendor.unref(filterResult).filters.type === "price" ? 1 : "",
        s: common_vendor.o(selectPriceSort)
      } : {}, {
        t: (_a = common_vendor.unref(brandList)[common_vendor.unref(filterResult).brand.index]) == null ? void 0 : _a.tag
      }, ((_b = common_vendor.unref(brandList)[common_vendor.unref(filterResult).brand.index]) == null ? void 0 : _b.tag) ? {
        v: common_vendor.f(common_vendor.unref(brandList)[common_vendor.unref(filterResult).brand.index].tag, (item, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(item),
            b: common_vendor.unref(brandList)[common_vendor.unref(filterResult).brand.index].childBrand && item === "品牌"
          }, common_vendor.unref(brandList)[common_vendor.unref(filterResult).brand.index].childBrand && item === "品牌" ? {
            c: "dd0caf51-2-" + i0,
            d: common_vendor.p({
              size: "12rpx",
              name: common_vendor.unref(isShowChildBrand) ? "up" : "down"
            })
          } : {}, {
            e: isTagSelected(item, common_vendor.unref(filterResult).brand.index) && item !== "品牌" ? 1 : "",
            f: index,
            g: common_vendor.o(($event) => toggleTag(item, common_vendor.unref(filterResult).brand.index), index)
          });
        })
      } : {}, {
        w: common_vendor.unref(isShowChildBrand)
      }, common_vendor.unref(isShowChildBrand) ? {
        x: common_vendor.f(common_vendor.unref(brandList)[common_vendor.unref(filterResult).brand.index].childBrand, (item, index, i0) => {
          return {
            a: common_vendor.t(item),
            b: isBrandSelected(item) ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => toggleChildBrand(item), index)
          };
        }),
        y: common_vendor.o(resetAllSelection),
        z: common_vendor.o(confirmSelection)
      } : {}, {
        A: common_vendor.unref(filterResult).brand.index === 0 ? "160rpx" : "168rpx",
        B: common_vendor.unref(filterResult).brand.index === 0 ? "140rpx" : "280rpx",
        C: common_vendor.unref(isShowChildBrand)
      }, common_vendor.unref(isShowChildBrand) ? {} : {}, {
        D: common_vendor.unref(filterResult).brand.index === 0
      }, common_vendor.unref(filterResult).brand.index === 0 ? {} : {}, {
        E: common_vendor.sr("backToTopRef", "dd0caf51-5"),
        F: common_vendor.p({
          threshold: 300,
          position: "bottom-right",
          size: 70,
          ["background-color"]: "#cacaca",
          color: "#ffffff"
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-dd0caf51"]]);
wx.createPage(MiniProgramPage);
