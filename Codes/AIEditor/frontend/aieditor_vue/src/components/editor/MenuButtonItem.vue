<template>
    <el-button
      class="menu-button-item"
      @click="action"
      :title="title"
      link
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
    const iconUrl = ref(remixiconUrl)
    return {
      iconUrl
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

.remix {
  width: 1.25rem !important; /* 修改图标的宽度 */
  height: 1.25rem !important; /* 修改图标的高度 */
  fill: currentColor; /* 修改图标的颜色 */
}


</style>
