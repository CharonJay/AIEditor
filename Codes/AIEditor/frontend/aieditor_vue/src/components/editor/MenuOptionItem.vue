<template>
    <el-select style="width: 125px">
      <el-option
        v-for="item in options"
        class="menu-option-item"
        :class="{ 'is-active': isActive(item) }"
        @click="handleClick(item)"
        :label="item.label"
        :value="item.value"
        :title="item.title"
      />
    </el-select>
</template>

<script>
import remixiconUrl from 'remixicon/fonts/remixicon.symbol.svg'
import { ElSelect, ElOption } from 'element-plus';
import { ref } from "vue";

export default {
  name: 'MenuOptionItem',
  components: {
    ElSelect,
    ElOption
  },
  props: {
    icon: {
      type: String,
      required: false
    },
    type: {
      type: String,
      required: false
    },
    options: {
      type: Array,
      required: true
    },
  },
  setup() {
    const iconUrl = ref(remixiconUrl);
    const handleClick = (item) => {
      // 执行点击事件的逻辑，可以调用item中的action函数
      item.action();
    };
    const isActive = (item) => {
      return item.isActive(); // 返回isActive函数的结果
    };
    return {
      iconUrl,
      handleClick,
      isActive
    };
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
  bottom: 10rem;
  fill: currentColor; /* 修改图标的颜色 */
}


</style>
