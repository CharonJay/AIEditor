<template>
  <div class="TocPanelContainer">
    <!-- 控制面板的展开与收起，点击按钮切换 panelVisible 状态 -->
    <el-button class="toc-button" @click="togglePanel" type="primary">{{ panelVisible ? '收起目录' : '展开目录' }}</el-button>
    <el-divider class="format-editor-panel-divider"> </el-divider>
    <!-- 当 panelVisible 为 true 时显示目录组件 Toc，将 tocItems 和 editor 对象传递给 Toc 组件 -->
    <Toc v-if="panelVisible" :items="tocItems" class="table-of-contents" :editor="editor" />
  </div>
</template>

<script>

import Toc from "@/components/editor/Toc.vue";
export default {
  name: 'CustomToc', // 组件名称
  components: {
    Toc, // 注册 Toc 组件
  },
  props: {
    items: { // 父组件传递的目录项数组，默认为空数组
      type: Array,
      default: () => [],
    },
    editor: { // 父组件传递的编辑器对象，默认为 null
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      panelVisible: false, // 控制面板展开与收起的状态变量，默认为 false（收起）
      tocItems: [], // 存储目录项的数组
    };
  },
  methods: {
    togglePanel() {
      this.panelVisible = !this.panelVisible; // 切换 panelVisible 的状态，控制面板的展开与收起
    },
  },
  watch: {
    items(newItems) { // 监听父组件传递的 items 属性的变化
      this.tocItems = newItems; // 更新组件内部的 tocItems 数组，保持与父组件的数据同步
    },
  },
  mounted() {
    this.tocItems = this.items; // 组件挂载后，初始化 tocItems 数组，确保初始数据同步
  },
};
</script>

<style scoped>
.TocPanelContainer {
  position: relative; /* 需要相对定位以包含伪元素 */
  width: 76%;
  padding: 5px;
  height: 87vh;
  max-height: 87vh;
  margin-top: 10px;
  margin-right: 20px;
  background-color: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
              0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
              -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
  color: #0d0d0d;
}

.TocPanelContainer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.2; /* 设置透明度 */
  z-index: -1; /* 确保伪元素在背景层 */
  pointer-events: none; /* 确保伪元素不会影响鼠标事件 */
}
.format-editor-panel-divider{
  margin-top: 10px;
  margin-bottom: 10px;
}
.toc-button{
  margin-top: 15px;
  margin-left: 20px;
}

</style>