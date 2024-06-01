<template>
  <el-dropdown split-button type="primary" @click="handleClick">
    <el-button
        class="menu-button-item"
        :class="{ 'is-active': isActive ? isActive() : null }"
        type="text"
        @click="action"
        :title="title">
    </el-button>
    <svg class="remix">
      <use :xlink:href="`${iconUrl}#ri-${icon}`" />
    </svg>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item  v-for="item in options">
          {item.label}
        </el-dropdown-item>
        <el-dropdown-item>Action 1</el-dropdown-item>
        <el-dropdown-item>Action 2</el-dropdown-item>
        <el-dropdown-item>Action 3</el-dropdown-item>
        <el-dropdown-item>Action 4</el-dropdown-item>
        <el-dropdown-item>Action 5</el-dropdown-item>
      </el-dropdown-menu>
    </template>
   </el-dropdown>
</template>

<script>
import remixiconUrl from 'remixicon/fonts/remixicon.symbol.svg'
import {ElButton, ElDropdown, ElDropdownMenu, ElDropdownItem} from "element-plus";
import {ref} from "vue";

export default {
  name: 'MenuButtonItem',
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
    action: {
      type: Function,
      required: true
    },
    isActive: {
      type: Function,
      default: null
    },
    options: {
      type: Array,
      required: true
    },
  },
  setup() {
    const iconUrl = ref(remixiconUrl)
    return {
      iconUrl
    }
  }
}
</script>

<style scoped lang="scss">

</style>
