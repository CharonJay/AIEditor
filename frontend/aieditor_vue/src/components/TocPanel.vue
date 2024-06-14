<template>
  <div>
    <!-- 控制面板的展开与收起，点击按钮切换 panelVisible 状态 -->
    <el-button @click="togglePanel" type="primary">{{ panelVisible ? '收起目录' : '展开目录' }}</el-button>

    <!-- 当 panelVisible 为 true 时显示目录组件 Toc，将 tocItems 和 editor 对象传递给 Toc 组件 -->
    <Toc v-if="panelVisible" :items="tocItems" class="table-of-contents" :editor="editor" />
  </div>
</template>

<script>
import Toc from './Toc.vue'; // 引入 Toc.vue 组件

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
