<template>
    <div class="app">
    <div class="main-content">
      <RouterView>
      </RouterView>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    // 组件选项
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, Sans-serif, SimHei, Microsoft Yahei, Microsoft JhengHei, KaiTi, serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
</style>