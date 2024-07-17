<template>
  <el-dialog
      class="formatting-template-dialog"
      v-model="internalDialogVisible"
      :before-close="handleClose"
      width="1200"
  >
    <el-container>
      <!-- 左侧菜单栏 -->
      <el-aside class="formatting-template-dialog-left-aside">
        <el-menu
          :default-active="activeMenuItem"
          class="el-menu-vertical-demo"
          @select="handleMenuSelect"
        >
          <el-menu-item index="1">我的模板</el-menu-item>
          <el-menu-item index="2">官方推荐</el-menu-item>
        </el-menu>
      </el-aside>
      <!-- 主内容区域 -->
      <el-main class="formatting-template-dialog-main">
        <component :is="getContentComponent(activeMenuItem)"
                   @useFormat="handleUseFormat"/>
      </el-main>
    </el-container>
  </el-dialog>
</template>

<script lang="ts">
import { defineComponent, ref, Component } from 'vue';

// 导入各个选项的组件
import UserFormat from '@/components/editor/UserFormat.vue';
import OfficialFormat from '@/components/editor/OfficialFormat.vue';


export default defineComponent({
  name: "FormattingTemplateDialog",
  components: {
    UserFormat,
    OfficialFormat,

  },
  props: {
    formattingTemplateDiaLogVisible: {
      type: Boolean,
      required: true
    },
  },
  emits: ['formattingTemplateDiaLogVisible','useFormatEvent'],
  setup(props, context) {
    const internalDialogVisible = ref(props.formattingTemplateDiaLogVisible);
    const activeMenuItem = ref('1');

    // 关闭对话框
    const handleClose = (done: Function) => {
      internalDialogVisible.value = false;
      context.emit('formattingTemplateDiaLogVisible', false);
      done();
    };

    // 处理菜单选择
    const handleMenuSelect = (index: string) => {
      activeMenuItem.value = index;
    };

    // 根据菜单项返回对应的组件
    const getContentComponent = (index: string): Component => {
      switch(index) {
        case '1':
          return UserFormat;
        case '2':
          return OfficialFormat;
        default:
          return UserFormat;
      }
    };

    //使用模板
    const handleUseFormat = (cardId: string) => {
      context.emit('useFormatEvent', cardId);
    };

    return {
      internalDialogVisible,
      handleClose,
      activeMenuItem,
      handleMenuSelect,
      handleUseFormat,
      getContentComponent
    };
  }
});
</script>

<style scoped lang="scss">
.formatting-template-dialog {

}

.formatting-template-dialog-left-aside {
  width: 12rem; /* 相当于 200px */
}

.el-menu-item.is-active {
  background-color: #c3ecff !important; /* 修改背景颜色 */
  color: #36a4fe !important; /* 修改字体颜色 */
}

.formatting-template-dialog-main {
  display: flex;
  justify-content: flex-start;
  height: 40rem;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
