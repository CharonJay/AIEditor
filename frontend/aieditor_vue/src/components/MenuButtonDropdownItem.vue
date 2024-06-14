<template>
  <el-dropdown class="menu-button-dropdown" split-button type="primary" @command="handleDropdownClick" >
    <el-button
        class="menu-button-dropdown-button"
        type="text"
        @click="handleButtonClick"
        :title="title">
      <svg class="remix">
        <use :xlink:href="`${iconUrl}#ri-${icon}`" />
      </svg>
    </el-button>

    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item
            v-for="item in options"
            :key="item.value"
            :command="item.value">
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

export default {
  name: 'MenuButtonDropdown',
  components: {
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

<style scoped lang="scss">
.menu-button-dropdown {
  margin-top: 0.7rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  outline: none;
}
.menu-button-dropdown-button {
  display: inline-flex;
  width: 0.5rem;
  height: 1.75rem;
  background-color: transparent;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  margin-right: 0.25rem;
}
.remix {
  width: 1.5rem; /* 修改图标的宽度 */
  height: 1.5rem; /* 修改图标的高度 */
  fill: currentColor; /* 修改图标的颜色 */
}

</style>
