<template>
    <el-button
      class="menu-button-item"
      @click="action"
      :title="title"
      link
    >
        <i :class="`ri-${icon} icon ri-lg` "></i>
    </el-button>
</template>

<script>
import '@/assets/remixicon/remixicon.css'
import {ElButton} from 'element-plus'
import {ref} from "vue";

export default {
  name: 'MenuButtonItem',
  components: {
    ElButton
  },
  props: {
    icon: {
      type: String,
      required: false
    },
    title: {
      type: String,
      required: false
    },
    action: {
      type: Function,
      required: false
    },
  },
  setup() {
    return {
    }
  }
}
</script>

<style lang="scss">
.menu-button-item {
  width: 1.25rem;
  height: 0.5rem;
  padding: .25rem;
  margin-right: .25rem;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.icon {
  width: 1.5rem !important; /* 修改图标的宽度 */
  height: 0.75rem !important; /* 修改图标的高度 */
  fill: currentColor; /* 修改图标的颜色 */
}

</style>
