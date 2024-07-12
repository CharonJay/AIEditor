<template>
  <el-dropdown class="menu-dropdown-item" size="small" type="primary" @command="handleDropdownClick" trigger="click">
    <el-button
        class="menu-button-dropdown-button"
        link
        :title="title"
    >{{title}}
      <el-icon class="el-icon--right"><arrow-down /></el-icon>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu >
        <el-dropdown-item
            v-for="item in options"
            :key="item.value"
            :command="item.value"
            :style="{ fontFamily: item.value }">
          {{ item.label }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script>
import remixiconUrl from 'remixicon/fonts/remixicon.symbol.svg'
import { ElButton, ElDropdown, ElDropdownMenu, ElDropdownItem } from "element-plus";
import { ref } from "vue";
import {ArrowDown} from "@element-plus/icons-vue";

export default {
  name: 'MenuButtonDropdown',
  components: {
    ArrowDown,
    ElButton,
    ElDropdown,
    ElDropdownMenu,
    ElDropdownItem
  },
  props: {
    icon: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    options: {
      type: Array,
      required: true
    },
    action: {
      type: Function,
      required: true
    },
  },
  setup(props) {
    const iconUrl = ref(remixiconUrl);
    const selectedOption = ref(null);

    const handleDropdownClick = (value) => {
      selectedOption.value = value; // 只保存 item 的 value
      props.action(selectedOption.value); // 传递选中的 value 给 action 函数
    };

    const handleButtonClick = () => {
      props.action(selectedOption.value); // 传递选中的 value 给 action 函数
    };

    return {
      iconUrl,
      selectedOption,
      handleDropdownClick,
      handleButtonClick
    };
  }
};
</script>

<style lang="scss">

.menu-dropdown-item{
  height: 2.25rem;
  padding: 0 !important;
  display: inline-flex; /* 确保使用 Flexbox 布局 */
  margin-right: 0.25rem;
  align-items: center;
}

</style>
