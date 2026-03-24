"use strict";
const common_vendor = require("../../common/vendor.js");
const api_endAgent = require("../../api/endAgent.js");
if (!Array) {
  const _component_uni_easyinput = common_vendor.resolveComponent("uni-easyinput");
  const _component_uni_forms_item = common_vendor.resolveComponent("uni-forms-item");
  const _component_uni_data_picker = common_vendor.resolveComponent("uni-data-picker");
  const _component_uni_data_select = common_vendor.resolveComponent("uni-data-select");
  const _component_uni_forms = common_vendor.resolveComponent("uni-forms");
  const _component_uni_file_picker = common_vendor.resolveComponent("uni-file-picker");
  (_component_uni_easyinput + _component_uni_forms_item + _component_uni_data_picker + _component_uni_data_select + _component_uni_forms + _component_uni_file_picker)();
}
const _sfc_main = {
  __name: "add",
  setup(__props) {
    const formRef = common_vendor.ref(null);
    const formRef2 = common_vendor.ref(null);
    const brandId = common_vendor.ref(null);
    const isEdit = common_vendor.ref(false);
    const isView = common_vendor.ref(false);
    const formData = common_vendor.ref({
      coach_name: "",
      mobile: "",
      typeId: "",
      personality_icon: "",
      city_id: "",
      text: "",
      work_img: [],
      self_img: [],
      video: [],
      order_num: "",
      show_salenum: 1,
      is_work: 1
    });
    const rules = {
      coach_name: {
        rules: [
          { required: true, errorMessage: "请输入品牌名称" },
          { minLength: 2, errorMessage: "品牌名称至少2个字符" }
        ]
      },
      mobile: {
        rules: [
          { required: true, errorMessage: "请输入品牌联系人" },
          { pattern: /^1[3-9]\d{9}$/, errorMessage: "请输入正确的手机号" }
        ]
      },
      typeId: {
        rules: [{ required: true, errorMessage: "请选择分类类型" }]
      },
      city_id: {
        rules: [{ required: true, errorMessage: "请选择城市" }]
      }
    };
    const rules2 = {
      text: {
        rules: [{ required: true, errorMessage: "请输入品牌简介" }]
      },
      order_num: {
        rules: [{ required: true, errorMessage: "请输入虚拟订单量" }]
      },
      is_work: {
        rules: [{ required: true, errorMessage: "请选择是否售卖" }]
      }
    };
    const categoryOptions = common_vendor.ref([]);
    const channelOptions = common_vendor.ref([]);
    const cityOptions = common_vendor.ref([]);
    const initCity = async () => {
      const res = await api_endAgent.agentBrandCity();
      if (res.code === 200 && res.data) {
        cityOptions.value = res.data.map((item) => ({
          value: item.id,
          text: item.title
        }));
      }
    };
    const getAgent = async () => {
      const res = await api_endAgent.agentQd();
      if (res.code === 200 && res.data) {
        channelOptions.value = res.data.map((item) => ({
          value: item.id,
          text: item.title
        }));
      }
    };
    const coachType = async () => {
      try {
        const res = await api_endAgent.coachTypeSelect();
        if (res.code === 200 && res.data) {
          categoryOptions.value = formatTreeData(res.data);
        }
      } catch (e) {
        console.error("获取分类失败", e);
      }
    };
    const onCategoryChange = (e) => {
      console.log("选择的分类:", e.detail.value);
    };
    const formatTreeData = (list) => {
      if (!list || list.length === 0)
        return null;
      return list.map((item) => {
        return {
          text: item.title,
          value: item.id,
          // 如果有子节点，递归处理
          children: item.children && item.children.length > 0 ? formatTreeData(item.children) : null
        };
      });
    };
    const extractOneUrl = (item) => {
      if (!item)
        return "";
      if (typeof item === "string")
        return item;
      const path = item.attachment_path;
      if (path && typeof path === "string")
        return path;
      const url = item.url;
      if (typeof url === "string")
        return url;
      if (url && typeof url === "object" && url.attachment_path)
        return url.attachment_path;
      return "";
    };
    const getImgUrl = (img) => {
      if (!img)
        return "";
      if (Array.isArray(img) && img.length > 0)
        return extractOneUrl(img[0]);
      if (typeof img === "object")
        return extractOneUrl(img);
      return typeof img === "string" ? img : "";
    };
    const getImgUrls = (imgList) => {
      if (!imgList || !Array.isArray(imgList))
        return [];
      return imgList.map(extractOneUrl).filter(Boolean);
    };
    const handleUpload = async (event, field, uploadType) => {
      const paths = event.tempFilePaths || [];
      const files = event.tempFiles || [];
      if (paths.length === 0)
        return;
      const isMulti = field === "self_img";
      const uploadOne = async (tempFilePath, fileItem) => {
        var _a, _b;
        const res = await api_endAgent.upLoadImg(String(tempFilePath), uploadType);
        if (res.code !== 200)
          throw new Error(res.return_msg || "上传失败");
        const urlStr = typeof res.data === "string" ? res.data : ((_a = res.data) == null ? void 0 : _a.attachment_path) || ((_b = res.data) == null ? void 0 : _b.url) || "";
        return { url: urlStr, name: (fileItem == null ? void 0 : fileItem.name) || "file", extname: (fileItem == null ? void 0 : fileItem.extname) || "" };
      };
      common_vendor.index.showLoading({ title: "上传中...", mask: true });
      try {
        const uploaded = [];
        for (let i = 0; i < paths.length; i++) {
          const item = await uploadOne(paths[i], files[i]);
          uploaded.push(item);
        }
        common_vendor.index.hideLoading();
        if (isMulti) {
          formData.value[field] = [...formData.value[field] || [], ...uploaded];
        } else {
          formData.value[field] = uploaded.length > 0 ? [uploaded[0]] : [];
        }
        common_vendor.index.showToast({ title: "上传成功", icon: "success" });
      } catch (error) {
        common_vendor.index.hideLoading();
        if (!isMulti)
          formData.value[field] = [];
        common_vendor.index.showToast({ title: error.message || "上传失败", icon: "none" });
        console.error("上传异常:", error);
      }
    };
    const handleSubmit = async () => {
      try {
        await formRef.value.validate().catch((err) => {
          if (err)
            throw err[0].errorMessage;
        });
        await formRef2.value.validate().catch((err) => {
          if (err)
            throw err[0].errorMessage;
        });
        const workImgUrl = getImgUrl(formData.value.work_img);
        const selfImgUrls = getImgUrls(formData.value.self_img);
        if (!workImgUrl)
          throw "请上传品牌ICON";
        if (selfImgUrls.length === 0)
          throw "请上传品牌图片";
        const params = {
          ...formData.value,
          work_img: workImgUrl,
          self_img: selfImgUrls,
          video: getImgUrl(formData.value.video)
        };
        if (isEdit.value) {
          params.id = brandId.value;
        }
        common_vendor.index.showLoading({ title: "提交中...", mask: true });
        const res = isEdit.value ? await api_endAgent.agentEditBrand(params) : await api_endAgent.agentAddBrand(params);
        common_vendor.index.hideLoading();
        if (res.code === 200) {
          const msg = isEdit.value ? "编辑成功" : "新增成功";
          common_vendor.index.showToast({ title: msg, icon: "success" });
          setTimeout(() => common_vendor.index.navigateBack(), 1500);
        } else {
          common_vendor.index.showToast({ title: res.return_msg || "操作失败", icon: "none" });
        }
      } catch (msg) {
        common_vendor.index.showToast({ title: msg || "请完善信息", icon: "none" });
      }
    };
    const handleCancel = () => {
      common_vendor.index.navigateBack();
    };
    const loadBrandDetail = (brand) => {
      if (!brand)
        return;
      formData.value.coach_name = brand.coach_name || "";
      formData.value.mobile = brand.mobile || "";
      formData.value.typeId = brand.type_id || "";
      formData.value.personality_icon = brand.personality_icon || "";
      formData.value.city_id = brand.city_id || "";
      formData.value.text = brand.text || "";
      formData.value.order_num = brand.order_num || "";
      formData.value.show_salenum = brand.show_salenum || 1;
      formData.value.is_work = brand.is_work || 1;
      if (brand.work_img) {
        formData.value.work_img = [{ url: brand.work_img, name: "work_img" }];
      }
      if (brand.self_img) {
        if (Array.isArray(brand.self_img)) {
          formData.value.self_img = brand.self_img.map((url) => ({ url, name: "self_img" }));
        } else if (typeof brand.self_img === "string") {
          formData.value.self_img = [{ url: brand.self_img, name: "self_img" }];
        }
      }
      if (brand.video) {
        formData.value.video = [{ url: brand.video, name: "video" }];
      }
    };
    common_vendor.onLoad((options) => {
      if (options == null ? void 0 : options.id) {
        brandId.value = options.id;
        if ((options == null ? void 0 : options.view) === "1") {
          isView.value = true;
          common_vendor.index.setNavigationBarTitle({ title: "查看品牌" });
        } else {
          isEdit.value = true;
          common_vendor.index.setNavigationBarTitle({ title: "编辑品牌" });
        }
        api_endAgent.agentViewBrand({ id: options.id }).then((res) => {
          if (res.code === 200 && res.data) {
            loadBrandDetail(res.data);
          }
        }).catch((e) => {
          console.error("获取品牌详情失败:", e);
        });
      } else {
        common_vendor.index.setNavigationBarTitle({ title: "新增品牌" });
      }
    });
    common_vendor.onMounted(() => {
      initCity();
      getAgent();
      coachType();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(($event) => formData.value.coach_name = $event),
        b: common_vendor.p({
          disabled: isView.value,
          placeholder: "请输入品牌名称",
          maxlength: "15",
          clearable: true,
          modelValue: formData.value.coach_name
        }),
        c: common_vendor.p({
          label: "品牌名称",
          name: "coach_name",
          required: true
        }),
        d: common_vendor.o(($event) => formData.value.mobile = $event),
        e: common_vendor.p({
          disabled: isView.value,
          placeholder: "请输入品牌联系人手机号",
          maxlength: "11",
          clearable: true,
          modelValue: formData.value.mobile
        }),
        f: common_vendor.p({
          label: "品牌联系人",
          name: "mobile",
          required: true
        }),
        g: common_vendor.o(onCategoryChange),
        h: common_vendor.o(($event) => formData.value.typeId = $event),
        i: common_vendor.p({
          disabled: isView.value,
          localdata: categoryOptions.value,
          ["popup-title"]: "请选择分类",
          placeholder: "请选择分类类型",
          modelValue: formData.value.typeId
        }),
        j: common_vendor.p({
          label: "分类类型",
          name: "typeId",
          required: true
        }),
        k: common_vendor.o(($event) => formData.value.personality_icon = $event),
        l: common_vendor.p({
          disabled: isView.value,
          localdata: channelOptions.value,
          placeholder: "请选择接口渠道",
          modelValue: formData.value.personality_icon
        }),
        m: common_vendor.p({
          label: "接口渠道",
          name: "personality_icon"
        }),
        n: common_vendor.o(($event) => formData.value.city_id = $event),
        o: common_vendor.p({
          disabled: isView.value,
          localdata: cityOptions.value,
          placeholder: "请选择城市",
          modelValue: formData.value.city_id
        }),
        p: common_vendor.p({
          label: "品牌上架城市",
          name: "city_id",
          required: true
        }),
        q: common_vendor.sr(formRef, "08b9a81a-0", {
          "k": "formRef"
        }),
        r: common_vendor.p({
          model: formData.value,
          rules,
          ["err-show-type"]: "none"
        }),
        s: common_vendor.o(($event) => formData.value.text = $event),
        t: common_vendor.p({
          disabled: isView.value,
          type: "textarea",
          placeholder: "请输入品牌简介",
          maxlength: 800,
          clearable: true,
          modelValue: formData.value.text
        }),
        v: common_vendor.p({
          label: "品牌简介",
          name: "text",
          required: true
        }),
        w: common_vendor.o((e) => handleUpload(e, "work_img", "picture")),
        x: common_vendor.o(($event) => formData.value.work_img = $event),
        y: common_vendor.p({
          disabled: isView.value,
          fileMediatype: "image",
          mode: "grid",
          limit: 1,
          ["auto-upload"]: false,
          modelValue: formData.value.work_img
        }),
        z: common_vendor.p({
          label: "品牌ICON",
          name: "work_img",
          required: true
        }),
        A: common_vendor.o((e) => handleUpload(e, "self_img", "picture")),
        B: common_vendor.o(($event) => formData.value.self_img = $event),
        C: common_vendor.p({
          disabled: isView.value,
          fileMediatype: "image",
          mode: "grid",
          limit: 3,
          ["auto-upload"]: false,
          modelValue: formData.value.self_img
        }),
        D: common_vendor.p({
          label: "品牌图片(最多上传三张)",
          name: "self_img",
          required: true
        }),
        E: common_vendor.o((e) => handleUpload(e, "video", "video")),
        F: common_vendor.o(($event) => formData.value.video = $event),
        G: common_vendor.p({
          disabled: isView.value,
          fileMediatype: "video",
          mode: "grid",
          limit: 1,
          ["auto-upload"]: false,
          modelValue: formData.value.video
        }),
        H: common_vendor.p({
          label: "品牌视频",
          name: "video"
        }),
        I: common_vendor.o(($event) => formData.value.order_num = $event),
        J: common_vendor.p({
          disabled: isView.value,
          type: "number",
          placeholder: "请输入虚拟订单量",
          clearable: true,
          modelValue: formData.value.order_num
        }),
        K: common_vendor.p({
          label: "虚拟订单量",
          name: "order_num",
          required: true
        }),
        L: isView.value,
        M: formData.value.show_salenum === 0,
        N: common_vendor.o(($event) => formData.value.show_salenum = $event.detail.checked ? 0 : 1),
        O: isView.value,
        P: formData.value.is_work === 1,
        Q: common_vendor.o((e) => {
          if (e.detail.checked)
            formData.value.is_work = 1;
        }),
        R: isView.value,
        S: formData.value.is_work === 0,
        T: common_vendor.o((e) => {
          if (e.detail.checked)
            formData.value.is_work = 0;
        }),
        U: common_vendor.p({
          label: "是否售卖",
          name: "is_work",
          required: true
        }),
        V: common_vendor.sr(formRef2, "08b9a81a-11", {
          "k": "formRef2"
        }),
        W: common_vendor.p({
          model: formData.value,
          rules: rules2
        }),
        X: !isView.value
      }, !isView.value ? {
        Y: common_vendor.t(isEdit.value ? "编辑" : "提交"),
        Z: common_vendor.o(handleSubmit),
        aa: common_vendor.t(isView.value ? "返回" : "返回"),
        ab: common_vendor.o(handleCancel)
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-08b9a81a"]]);
wx.createPage(MiniProgramPage);
