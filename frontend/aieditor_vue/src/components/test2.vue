<template>
    <el-option
      v-for="item in options"
      class="menu-option-item"
      :class="{ 'is-active': isActive ? isActive() : null }"
      @click.native="item.action"
      :title="item.title"
      :label="item.label"
      :value="item.value"
      :disabled="item.disabled"
      :teleported="false"
    />
    <svg class="remix">
      <use :xlink:href="`${iconUrl}#ri-${icon}`" />
    </svg>
</template>

<script>
import remixiconUrl from 'remixicon/fonts/remixicon.symbol.svg'
import { ElSelect, ElOption } from 'element-plus';
import {ref} from "vue";

export default {
  name: 'MenuOptionItem',
  components: {
    ElSelect,
    ElOption
  },
  props: {
    options: {
      type: String,
      required: false
    },
    action: {
      type: Function,
      required: true
    },
    isActive: {
      type: Function,
      default: null
    }
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
.menu-item {
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
