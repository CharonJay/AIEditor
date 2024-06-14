<template>
    <el-button
      class="menu-button-item"
      @click="action"
      :title="title"
      type="text"
    >
    <svg class="remix">
      <use :xlink:href="`${iconUrl}#ri-${icon}`" />
    </svg>
    </el-button>
</template>

<script>
import remixiconUrl from 'remixicon/fonts/remixicon.symbol.svg'
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
  },
  setup() {
    const iconUrl = ref(remixiconUrl)
    return {
      iconUrl
    }
  }
}
</script>

<style lang="scss">
.menu-button-item {
  width: 1.75rem;
  height: 1.75rem;
  padding: .25rem;
  margin-right: .25rem;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.remix {
  width: 1.5rem; /* 修改图标的宽度 */
  height: 1.5rem; /* 修改图标的高度 */
  fill: currentColor; /* 修改图标的颜色 */
}

.is-active,
.el-button:hover {
  color: #0c67e1;
  background-color: rgba(10, 3, 3, 0.49);
}
</style>
