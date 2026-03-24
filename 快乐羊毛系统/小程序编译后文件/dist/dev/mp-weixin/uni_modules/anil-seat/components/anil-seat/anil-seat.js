"use strict";
const common_vendor = require("../../../../common/vendor.js");
const common_assets = require("../../../../common/assets.js");
const _sfc_main = {
  name: "anil-seat",
  props: {
    seatData: {
      type: Array
    },
    max: {
      type: Number,
      default: 4
    },
    title: {
      type: String,
      default: ""
    },
    info: {
      type: String,
      default: ""
    },
    roomName: {
      type: String,
      default: ""
    },
    height: {
      type: String,
      default: "100vh"
    }
  },
  data() {
    return {
      scaleMin: 1,
      //h5端为解决1无法缩小问题，设为0.95
      boxWidth: 400,
      //屏幕宽度px
      space: " ",
      //空格
      seatArray: [],
      //影院座位的二维数组,-1为非座位，0为未购座位，1为已选座位(绿色),2为已购座位(红色),一维行，二维列
      seatRow: 0,
      //影院座位行数
      seatCol: 0,
      //影院座位列数
      seatSize: 0,
      //座位尺寸
      SelectNum: 0,
      //选择座位数
      moveX: 0,
      //水平移动偏移量
      scale: 1,
      //放大倍数
      minRow: 0,
      //从第几行开始排座位
      minCol: 0,
      //从第几列开始排座位
      showTis: true,
      //显示选座提示
      seatList: [],
      //接口获取的原始位置
      mArr: [],
      //排数提示
      optArr: [],
      //选中的座位数组。
      isWXAPP: false,
      areaHeight: 0,
      indicatorLeft: 0,
      // 指示器距离左侧的距离
      scrollRate: 0
      // 滚动比例
    };
  },
  computed: {
    aPrice() {
      let totalAmount = "";
      if (this.optArr && this.optArr.length) {
        totalAmount = this.optArr.map((item) => Number(item.Price)).reduce((prev, curr) => prev + curr);
      }
      return Number(totalAmount).toFixed(2);
    },
    rpxNum() {
      return this.boxWidth / 750;
    },
    pxNum() {
      return 750 / this.boxWidth;
    }
  },
  created() {
    common_vendor.index.getSystemInfo({
      success: (e) => {
        this.boxWidth = e.screenWidth;
      }
    });
  },
  methods: {
    initData: function(data) {
      let arr = data || this.seatData;
      let row = 0;
      let col = 0;
      let minCol = parseInt(arr[0].XCoord);
      let minRow = parseInt(arr[0].YCoord);
      for (let i of arr) {
        minRow = parseInt(i.YCoord) < minRow ? parseInt(i.YCoord) : minRow;
        minCol = parseInt(i.XCoord) < minCol ? parseInt(i.XCoord) : minCol;
        row = parseInt(i.YCoord) > row ? parseInt(i.YCoord) : row;
        col = parseInt(i.XCoord) > col ? parseInt(i.XCoord) : col;
      }
      this.seatList = arr;
      this.seatRow = row - minRow + 1;
      this.seatCol = col - minCol + 3;
      this.minRow = minRow;
      this.minCol = minCol - 1;
      this.initSeatArray();
    },
    initSeatArray: function() {
      let seatArray = Array(this.seatRow).fill(0).map(
        () => Array(this.seatCol).fill({
          type: -1,
          SeatCode: "",
          RowNum: "",
          ColumnNum: ""
        })
      );
      this.seatArray = seatArray;
      this.seatSize = this.boxWidth > 0 ? parseInt(parseInt(this.boxWidth, 10) / (this.seatCol + 1), 10) : parseInt(parseInt(414, 10) / (this.seatCol + 1), 10);
      this.initNonSeatPlace();
    },
    initNonSeatPlace: function() {
      let seat = this.seatList.slice();
      let arr = this.seatArray.slice();
      for (let num in seat) {
        let status = 2;
        switch (seat[num].Status) {
          case -2:
            status = 2;
            break;
          case -1:
            status = -1;
            break;
          case 0:
            status = 2;
            break;
          case 1:
            status = 0;
            break;
        }
        arr[parseInt(seat[num].YCoord) - this.minRow][parseInt(seat[num].XCoord) - this.minCol] = {
          type: status,
          SeatCode: seat[num].SeatCode,
          RowNum: seat[num].RowNum,
          ColumnNum: seat[num].ColumnNum,
          Price: seat[num].Price,
          SeatName: seat[num].SeatName,
          flag: seat[num].flag,
          area: seat[num].area
        };
      }
      this.seatArray = arr.slice();
      let mArr = [];
      for (let i in arr) {
        let m = "";
        for (let n of arr[i]) {
          if (n.SeatCode) {
            m = n.RowNum;
          }
        }
        mArr.push(m || "");
      }
      this.mArr = mArr;
    },
    onScale: function(e) {
      this.showTis = false;
      let w = this.boxWidth * 0.5;
      let s = 1 - e.detail.scale;
      this.moveX = w * s;
      this.scale = e.detail.scale;
      if (s >= 0) {
        this.showTis = true;
      }
    },
    onMove: function(e) {
      this.showTis = false;
      this.moveX = e.detail.x;
    },
    resetSeat: function() {
      this.SelectNum = 0;
      this.optArr = [];
      let oldArray = this.seatArray.slice();
      for (let i = 0; i < this.seatRow; i++) {
        for (let j = 0; j < this.seatCol; j++) {
          if (oldArray[i][j].type === 1) {
            oldArray[i][j].type = 0;
          }
        }
      }
      this.seatArray = oldArray;
    },
    buySeat: function() {
      if (this.SelectNum === 0)
        return;
      this.$emit("confirm", this.optArr);
    },
    handleChooseSeat: function(row, col, isbreak) {
      let newArray = this.seatArray;
      let seatValue = newArray[row][col].type;
      let flag = newArray[row][col].flag;
      if (seatValue === 2 || seatValue === -1)
        return;
      if (seatValue === 1) {
        newArray[row][col].type = 0;
        this.SelectNum--;
        this.getOptArr(newArray[row][col], 0);
      } else if (seatValue === 0) {
        if (this.SelectNum >= this.max) {
          return common_vendor.index.showToast({
            title: "一次最多选择" + this.max + "张",
            icon: "none"
          });
        }
        newArray[row][col].rowIndex = row;
        newArray[row][col].colIndex = col;
        newArray[row][col].type = 1;
        this.SelectNum++;
        this.getOptArr(newArray[row][col], 1);
      }
      if (flag === 1 && !isbreak)
        this.handleChooseSeat(row, col + 1, true);
      if (flag === 2 && !isbreak)
        this.handleChooseSeat(row, col - 1, true);
    },
    // --- 核心修复：合并后的 getOptArr ---
    getOptArr: function(item, type) {
      let currentArr = this.optArr;
      if (type === 1) {
        currentArr.push(item);
      } else if (type === 0) {
        let arr = [];
        currentArr.forEach((v) => {
          if (v.SeatCode !== item.SeatCode) {
            arr.push(v);
          }
        });
        currentArr = arr;
      }
      this.optArr = currentArr.slice();
      if (this.optArr.length <= 4) {
        this.indicatorLeft = 0;
      }
    },
    // --- 核心修复：滚动条计算 ---
    onScrollSeat(e) {
      const { scrollLeft, scrollWidth } = e.detail;
      const viewWidth = this.boxWidth * 0.93;
      const maxScroll = scrollWidth - viewWidth;
      if (maxScroll <= 0) {
        this.indicatorLeft = 0;
        return;
      }
      const rate = scrollLeft / maxScroll;
      this.indicatorLeft = rate * 30;
    },
    smartChoose: function(num) {
      this.resetSeat();
      let rowStart = parseInt((this.seatRow - 1) / 2, 10) + 1;
      let backResult = this.searchSeatByDirection(
        rowStart,
        this.seatRow - 1,
        num
      );
      if (backResult.length > 0) {
        this.chooseSeat(backResult);
        this.SelectNum += num;
        return;
      }
      let forwardResult = this.searchSeatByDirection(rowStart - 1, 0, num);
      if (forwardResult.length > 0) {
        this.chooseSeat(forwardResult);
        this.SelectNum += num;
        return;
      }
      common_vendor.index.showToast({ title: "无合法位置可选!", icon: "none" });
    },
    searchSeatByDirection: function(fromRow, toRow, num) {
      let currentDirectionSearchResult = [];
      let largeRow = fromRow > toRow ? fromRow : toRow, smallRow = fromRow > toRow ? toRow : fromRow;
      for (let i = smallRow; i <= largeRow; i++) {
        let tempRowResult = [], minDistanceToMidLine = Infinity;
        try {
          for (let j = 0; j <= this.seatCol - num; j++) {
            if (this.checkRowSeatContinusAndEmpty(i, j, j + num - 1, num)) {
              let resultMidPos = parseInt(j + num / 2, 10);
              let distance = Math.abs(
                parseInt(this.seatCol / 2) - resultMidPos
              );
              if (distance < minDistanceToMidLine) {
                minDistanceToMidLine = distance;
                tempRowResult = this.generateRowResult(i, j, j + num - 1);
              }
            }
          }
        } catch (e) {
        }
        currentDirectionSearchResult.push({
          result: tempRowResult,
          offset: minDistanceToMidLine
        });
      }
      let isBackDir = fromRow < toRow;
      let finalReuslt = [], minDistanceToMid = Infinity;
      if (isBackDir) {
        currentDirectionSearchResult.forEach((item) => {
          if (item.offset < minDistanceToMid) {
            finalReuslt = item.result;
            minDistanceToMid = item.offset;
          }
        });
      } else {
        currentDirectionSearchResult.reverse().forEach((item) => {
          if (item.offset < minDistanceToMid) {
            finalReuslt = item.result;
            minDistanceToMid = item.offset;
          }
        });
      }
      return finalReuslt;
    },
    checkRowSeatContinusAndEmpty: function(rowNum, startPos, endPos, num) {
      let isValid = true;
      for (let i = startPos; i <= endPos; i++) {
        if (!this.seatArray[rowNum][i] || this.seatArray[rowNum][i].type !== 0) {
          isValid = false;
          break;
        }
        if ([1, 2].includes(this.seatArray[rowNum][i].flag)) {
          isValid = false;
          break;
        }
      }
      return isValid;
    },
    generateRowResult: function(row, startPos, endPos) {
      let result = [];
      for (let i = startPos; i <= endPos; i++) {
        result.push([row, i]);
      }
      return result;
    },
    chooseSeat: function(result) {
      let oldArray = this.seatArray.slice();
      for (let i = 0; i < result.length; i++) {
        oldArray[result[i][0]][result[i][1]].rowIndex = result[i][0];
        oldArray[result[i][0]][result[i][1]].colIndex = result[i][1];
        oldArray[result[i][0]][result[i][1]].type = 1;
        this.optArr.push(oldArray[result[i][0]][result[i][1]]);
      }
      this.seatArray = oldArray;
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.s("width:" + $data.seatSize + "px;height:" + $data.seatSize + "px"),
    b: common_assets._imports_0,
    c: common_vendor.s("width:" + $data.seatSize + "px;height:" + $data.seatSize + "px"),
    d: common_assets._imports_1,
    e: common_vendor.s("width:" + $data.seatSize + "px;height:" + $data.seatSize + "px"),
    f: common_assets._imports_2,
    g: common_vendor.t($props.roomName),
    h: common_vendor.f($data.seatArray, (item, index, i0) => {
      return {
        a: common_vendor.f(item, (seat, col, i1) => {
          return common_vendor.e({
            a: seat.flag === 1
          }, seat.flag === 1 ? common_vendor.e({
            b: seat.type === 0
          }, seat.type === 0 ? {
            c: common_assets._imports_3
          } : seat.type === 1 ? {
            e: common_assets._imports_4
          } : seat.type === 2 ? {
            g: common_assets._imports_1
          } : {}, {
            d: seat.type === 1,
            f: seat.type === 2
          }) : seat.flag === 2 ? common_vendor.e({
            i: seat.type === 0
          }, seat.type === 0 ? {
            j: common_assets._imports_5
          } : seat.type === 1 ? {
            l: common_assets._imports_6
          } : seat.type === 2 ? {
            n: common_assets._imports_1
          } : {}, {
            k: seat.type === 1,
            m: seat.type === 2
          }) : common_vendor.e({
            o: seat.type === 0
          }, seat.type === 0 ? {
            p: common_assets._imports_0
          } : seat.type === 1 ? {
            r: common_assets._imports_2
          } : seat.type === 2 ? {
            t: common_assets._imports_1
          } : {}, {
            q: seat.type === 1,
            s: seat.type === 2
          }), {
            h: seat.flag === 2,
            v: col,
            w: common_vendor.o(($event) => $options.handleChooseSeat(index, col), col)
          });
        }),
        b: index
      };
    }),
    i: common_vendor.s("width:" + $data.seatSize + "px;height:" + $data.seatSize + "px"),
    j: common_vendor.s("width:" + $data.boxWidth + "px;height:" + $data.seatSize + "px"),
    k: common_vendor.f($data.mArr, (m, mindex, i0) => {
      return {
        a: common_vendor.t(m),
        b: mindex
      };
    }),
    l: common_vendor.s("height:" + $data.seatSize + "px;"),
    m: common_vendor.s("left: " + (10 - $data.moveX / $data.scale) + "px;"),
    n: common_vendor.s("width: 750rpx;height:" + ($data.seatRow * 40 + 350) + "rpx;"),
    o: common_vendor.o((...args) => $options.onMove && $options.onMove(...args)),
    p: common_vendor.o((...args) => $options.onScale && $options.onScale(...args)),
    q: common_vendor.t($props.title),
    r: common_vendor.t($props.info),
    s: $data.SelectNum === 0
  }, $data.SelectNum === 0 ? {
    t: common_vendor.f(Math.min($props.max, 6), (num, k0, i0) => {
      return {
        a: common_vendor.t(num + 1),
        b: num,
        c: common_vendor.o(($event) => $options.smartChoose(num + 1), num)
      };
    })
  } : common_vendor.e({
    v: common_vendor.f($data.optArr, (optItem, optindex, i0) => {
      return {
        a: common_vendor.t(optItem.SeatName),
        b: common_vendor.t(optItem.Price || ""),
        c: optItem.SeatCode,
        d: common_vendor.o(($event) => $options.handleChooseSeat(optItem.rowIndex, optItem.colIndex), optItem.SeatCode)
      };
    }),
    w: $data.optArr.length > 4
  }, $data.optArr.length > 4 ? {
    x: $data.indicatorLeft + "rpx"
  } : {}), {
    y: common_vendor.t($data.SelectNum === 0 ? "来选座位吧~" : `￥ ${$options.aPrice} 确认座位`),
    z: $data.SelectNum === 0 ? 1 : "",
    A: common_vendor.o((...args) => $options.buySeat && $options.buySeat(...args)),
    B: $props.height
  });
}
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render]]);
wx.createComponent(Component);
