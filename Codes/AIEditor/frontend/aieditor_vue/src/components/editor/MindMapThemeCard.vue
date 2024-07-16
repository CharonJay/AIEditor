<template>
  <el-container class="mind-map-theme-card-container">
    <el-card class="mind-map-theme-card" shadow="hover">
      <template #header>
        <div class="custom-card-header">{{ cardTitle }}</div>
      </template>
      <img
        :src="imgSrc"
        class="mind-map-theme-card-image"
        alt="展示图片"/>
      <template #footer>
        <div class="custom-card-footer">
          <el-button class="mind-map-theme-card-button" type="primary" text @click="onUse">使用</el-button>
        </div>
      </template>
    </el-card>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: "MindMapThemeCard",
  props: {
    cardId:{
      type: String,
      required: true
    },
    cardTitle: {
      type: String,
      required: true
    },
    imgSrc: {
      type: String,
      required: true
    }
  },
  setup(props, context) {
    const onUse = () => {
      context.emit('useThemeEvent', props.cardId);
    };

    return {
      onUse
    };
  }
});
</script>

<style scoped lang="scss">
.mind-map-theme-card-container {
  width: 28rem;
  height: 8rem;
}
.mind-map-theme-card {
  width: 100%;
  height: 100%;
}
.el-card :deep .el-card__header {
  height: 20%;
  padding: 0 !important;
}

.el-card :deep .el-card__body {
  width: 100%;
  height: 60%;
  padding: 0 !important;
}

.el-card :deep .el-card__footer {
  height: 20%;
  padding: 0 !important;
}

.mind-map-theme-card-image {
  width: 100%;
  height: 100%;
}

.mind-map-theme-card-button {
  margin-top: 0.25rem;
  width: 4rem !important;
  height: 1.5rem !important;
}

.custom-card-header {
  height: 100%;
  padding: 0;
  background-color: rgba(200, 230, 255, 0.65);
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-card-footer {
  height: 100%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
}
</style>
