"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = {
  __name: "selCity",
  setup(__props) {
    const rawCities = common_vendor.ref([
      { id: 1, name: "鞍山" },
      { id: 2, name: "北京" },
      { id: 3, name: "上海" },
      { id: 4, name: "广州" },
      { id: 5, name: "深圳" },
      { id: 6, name: "杭州" },
      { id: 7, name: "南京" },
      { id: 8, name: "武汉" },
      { id: 9, name: "成都" },
      { id: 10, name: "重庆" },
      { id: 11, name: "天津" },
      { id: 12, name: "西安" },
      { id: 13, name: "苏州" },
      { id: 14, name: "郑州" },
      { id: 15, name: "长沙" },
      { id: 16, name: "青岛" },
      { id: 17, name: "大连" },
      { id: 18, name: "昆明" },
      { id: 19, name: "沈阳" },
      { id: 20, name: "厦门" },
      { id: 21, name: "宁波" },
      { id: 22, name: "无锡" },
      { id: 23, name: "佛山" },
      { id: 24, name: "东莞" },
      { id: 25, name: "合肥" },
      { id: 26, name: "福州" },
      { id: 27, name: "乌鲁木齐" },
      { id: 28, name: " 齐齐哈尔" }
    ]);
    const citiesData = common_vendor.ref(rawCities.value.map((city) => {
      const py = common_vendor.pinyin(city.name, { toneType: "none" });
      return {
        ...city,
        pinyin: py.replace(/\s/g, ""),
        // 去除空格
        firstLetter: py.trim().charAt(0).toUpperCase()
      };
    }));
    const hotCityIds = [2, 3, 4, 5, 8, 9, 10, 14];
    const hotCities = common_vendor.computed(() => {
      const map = new Map(citiesData.value.map((c) => [c.id, c]));
      return hotCityIds.map((id) => map.get(id)).filter(Boolean);
    });
    const locationCity = common_vendor.ref({
      name: "定位中..."
    });
    const mockLocation = () => {
      common_vendor.index.getLocation({
        type: "wgs84"
      });
      setTimeout(() => {
        locationCity.value = { id: 2, name: "北京" };
      }, 800);
    };
    const cityGroups = common_vendor.computed(() => {
      const groups = {};
      citiesData.value.forEach((city) => {
        const letter = city.firstLetter;
        if (!groups[letter]) {
          groups[letter] = [];
        }
        groups[letter].push(city);
      });
      return Object.keys(groups).sort().map((letter) => ({
        letter,
        cities: groups[letter].sort((a, b) => a.pinyin.localeCompare(b.pinyin))
      }));
    });
    const sortedCityGroups = common_vendor.computed(() => cityGroups.value);
    const indexLetters = common_vendor.computed(() => {
      return cityGroups.value.map((g) => g.letter);
    });
    const currentLetter = common_vendor.ref("");
    const scrollIntoId = common_vendor.ref("");
    const searchText = common_vendor.ref("");
    const searchResult = common_vendor.ref([]);
    const handleSearchInput = (e) => {
      const keyword = e.detail.value.trim().toLowerCase();
      if (!keyword) {
        searchResult.value = [];
        return;
      }
      searchResult.value = citiesData.value.filter((city) => {
        return city.name.includes(keyword) || city.pinyin.includes(keyword);
      });
    };
    const handleSearch = (e) => {
      handleSearchInput(e);
    };
    const selectCity = (city) => {
      common_vendor.index.$emit("city", city);
      common_vendor.index.navigateBack();
    };
    const onIndexTouchStart = (e) => {
      const letter = e.currentTarget.dataset.letter;
      if (letter) {
        scrollToLetter(letter);
        currentLetter.value = letter;
      }
    };
    const onIndexTouchMove = (e) => {
      e.preventDefault();
      const touchY = e.touches[0].clientY;
      const query = common_vendor.index.createSelectorQuery();
      query.selectAll(".index-item").boundingClientRect((rects) => {
        if (!rects || rects.length === 0)
          return;
        for (let i = 0; i < rects.length; i++) {
          const rect = rects[i];
          if (touchY >= rect.top && touchY <= rect.bottom) {
            const letter = indexLetters.value[i];
            if (letter && currentLetter.value !== letter) {
              currentLetter.value = letter;
              scrollToLetter(letter);
            }
            break;
          }
        }
      }).exec();
    };
    const onIndexTouchEnd = () => {
      setTimeout(() => {
        currentLetter.value = "";
      }, 200);
    };
    const scrollToLetter = (letter) => {
      scrollIntoId.value = "letter-" + letter;
      common_vendor.nextTick$1(() => {
        scrollIntoId.value = "letter-" + letter;
      });
    };
    const debounce = (fn, delay) => {
      let timer = null;
      return function(...args) {
        if (timer)
          clearTimeout(timer);
        timer = setTimeout(() => {
          fn.apply(this, args);
        }, delay);
      };
    };
    let titleRects = [];
    const updateTitleRects = () => {
      return new Promise((resolve) => {
        const query = common_vendor.index.createSelectorQuery();
        query.selectAll(".letter-title").boundingClientRect((rects) => {
          titleRects = rects || [];
          resolve(rects);
        }).exec();
      });
    };
    const handleScroll = debounce(async (e) => {
      var _a, _b;
      if (searchResult.value.length > 0)
        return;
      if (titleRects.length === 0) {
        await updateTitleRects();
      }
      const scrollTop = e.detail.scrollTop;
      for (let i = 0; i < titleRects.length; i++) {
        const rect = titleRects[i];
        if (rect.bottom > scrollTop + 10) {
          const letter = (_a = cityGroups.value[i]) == null ? void 0 : _a.letter;
          if (letter && currentLetter.value !== letter) {
            currentLetter.value = letter;
          }
          break;
        }
        if (i === titleRects.length - 1) {
          const letter = (_b = cityGroups.value[i]) == null ? void 0 : _b.letter;
          if (letter && currentLetter.value !== letter) {
            currentLetter.value = letter;
          }
        }
      }
    }, 50);
    const listHeight = common_vendor.ref("600px");
    common_vendor.onMounted(() => {
      const systemInfo = common_vendor.index.getSystemInfoSync();
      listHeight.value = systemInfo.windowHeight - 80 + "px";
      mockLocation();
      setTimeout(() => {
        updateTitleRects();
      }, 200);
    });
    common_vendor.watch(cityGroups, () => {
      common_vendor.nextTick$1(() => {
        updateTitleRects();
      });
    }, { deep: true });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(handleSearch),
        b: common_vendor.o([($event) => common_vendor.isRef(searchText) ? searchText.value = $event.detail.value : null, handleSearchInput]),
        c: common_vendor.unref(searchText),
        d: common_vendor.unref(searchResult).length > 0
      }, common_vendor.unref(searchResult).length > 0 ? common_vendor.e({
        e: common_vendor.f(common_vendor.unref(searchResult), (item, k0, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: item.id,
            c: common_vendor.o(($event) => selectCity(item), item.id)
          };
        }),
        f: common_vendor.unref(searchResult).length === 0
      }, common_vendor.unref(searchResult).length === 0 ? {} : {}) : common_vendor.e({
        g: common_vendor.t(common_vendor.unref(locationCity).name),
        h: !common_vendor.unref(locationCity).name
      }, !common_vendor.unref(locationCity).name ? {} : {}, {
        i: common_vendor.o(($event) => selectCity(common_vendor.unref(locationCity))),
        j: common_vendor.f(common_vendor.unref(hotCities), (item, k0, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: item.id,
            c: common_vendor.o(($event) => selectCity(item), item.id)
          };
        }),
        k: common_vendor.f(common_vendor.unref(sortedCityGroups), (group, k0, i0) => {
          return {
            a: common_vendor.t(group.letter),
            b: "letter-" + group.letter,
            c: common_vendor.f(group.cities, (item, k1, i1) => {
              return {
                a: common_vendor.t(item.name),
                b: item.id,
                c: common_vendor.o(($event) => selectCity(item), item.id)
              };
            }),
            d: group.letter
          };
        })
      }), {
        l: common_vendor.unref(scrollIntoId),
        m: common_vendor.unref(listHeight),
        n: common_vendor.o((...args) => common_vendor.unref(handleScroll) && common_vendor.unref(handleScroll)(...args)),
        o: !common_vendor.unref(searchText)
      }, !common_vendor.unref(searchText) ? {
        p: common_vendor.f(common_vendor.unref(indexLetters), (item, k0, i0) => {
          return {
            a: common_vendor.t(item),
            b: item,
            c: common_vendor.unref(currentLetter) === item ? 1 : "",
            d: common_vendor.o(onIndexTouchStart, item),
            e: common_vendor.o(onIndexTouchMove, item),
            f: common_vendor.o(onIndexTouchEnd, item),
            g: item
          };
        })
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-869706cf"]]);
wx.createPage(MiniProgramPage);
