"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Math) {
  (Icon + Navbar)();
}
const Navbar = () => "../../components/NavBar/Navbar.js";
const Icon = () => "../../components/Icon/Icon.js";
const _sfc_main = {
  __name: "search",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const backUrl = () => {
      common_vendor.index.navigateBack();
    };
    const searchKeyword = common_vendor.ref("");
    const showSearchContent = common_vendor.ref(false);
    const searchHistory = common_vendor.ref([]);
    const getSearchHistory = () => {
      try {
        const history = common_vendor.index.getStorageSync("searchHistory");
        return history ? history : [];
      } catch (e) {
        return [];
      }
    };
    const saveSearchHistory = (history) => {
      try {
        common_vendor.index.setStorageSync("searchHistory", history);
      } catch (e) {
      }
    };
    common_vendor.onMounted(() => {
      searchHistory.value = getSearchHistory();
    });
    const hotSearchList = common_vendor.reactive([
      { keyword: "iPhone 15", searchCount: 12345 },
      { keyword: "华为Mate60", searchCount: 10234 },
      { keyword: "小米14", searchCount: 9876 },
      { keyword: "MacBook Pro", searchCount: 8765 },
      { keyword: "AirPods Pro", searchCount: 7654 },
      { keyword: "Switch游戏机", searchCount: 6543 },
      { keyword: "戴尔显示器", searchCount: 5432 },
      { keyword: "机械键盘", searchCount: 4321 }
    ]);
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
      addToHistory(searchKeyword.value);
      goToSearchResult(searchKeyword.value);
    };
    const searchFromHistory = (keyword) => {
      searchKeyword.value = keyword;
      addToHistory(keyword);
      goToSearchResult(keyword);
    };
    const delHistory = (index) => {
      searchHistory.value.splice(index, 1);
      common_vendor.index.setStorageSync("searchHistory", searchHistory.value);
    };
    const searchFromHot = (keyword) => {
      searchKeyword.value = keyword;
      addToHistory(keyword);
      goToSearchResult(keyword);
    };
    const selectSuggestion = (keyword) => {
      searchKeyword.value = keyword;
      addToHistory(keyword);
      goToSearchResult(keyword);
    };
    const goToSearchResult = (keyword) => {
      searchKeyword.value = "";
      searchSuggestions.value = [];
      showSearchContent.value = false;
      common_vendor.index.navigateTo({
        url: `/subPages/search/searchResult?keyword=${encodeURIComponent(keyword)}`
      });
    };
    const clearKeyword = () => {
      searchKeyword.value = "";
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
      searchHistory.value = history;
    };
    const clearHistory = () => {
      common_vendor.index.showModal({
        title: "确认清空",
        content: "确定要清空搜索历史吗？",
        success: (res) => {
          if (res.confirm) {
            saveSearchHistory([]);
            searchHistory.value = [];
          }
        }
      });
    };
    return (_ctx, _cache) => {
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
            a: "7274e98b-2-" + i0,
            b: common_vendor.f(item.highlightedHtml.parts, (part, partIndex, i1) => {
              return {
                a: common_vendor.t(part.text),
                b: partIndex,
                c: part.isHighlighted ? "#fa6400" : "#333"
              };
            }),
            c: index,
            d: common_vendor.o(($event) => selectSuggestion(item.text), index)
          };
        }),
        j: common_vendor.p({
          name: "search2",
          size: "40rpx",
          color: "#999"
        })
      } : {}, {
        k: !common_vendor.unref(showSearchContent) && !common_vendor.unref(searchKeyword)
      }, !common_vendor.unref(showSearchContent) && !common_vendor.unref(searchKeyword) ? common_vendor.e({
        l: common_vendor.unref(searchHistory).length > 0
      }, common_vendor.unref(searchHistory).length > 0 ? {
        m: common_vendor.p({
          name: "delet",
          size: "36rpx"
        }),
        n: common_vendor.o(clearHistory),
        o: common_vendor.f(common_vendor.unref(searchHistory), (item, index, i0) => {
          return {
            a: common_vendor.t(item),
            b: index,
            c: common_vendor.o(($event) => delHistory(index), index),
            d: common_vendor.o(($event) => searchFromHistory(item), index)
          };
        })
      } : {}, {
        p: common_vendor.f(common_vendor.unref(hotSearchList), (item, index, i0) => {
          return {
            a: common_vendor.t(item.keyword),
            b: index,
            c: index < 3 ? 1 : "",
            d: common_vendor.o(($event) => searchFromHot(item.keyword), index)
          };
        })
      }) : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-7274e98b"]]);
wx.createPage(MiniProgramPage);
