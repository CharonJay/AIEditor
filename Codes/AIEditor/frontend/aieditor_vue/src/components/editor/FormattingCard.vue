<template>
  <el-container class="formatting-card-container">
    <el-card class="formatting-card-card" shadow="hover">
      <template #header>
        {{ cardTitle }}
      </template>
      <img
        :src="imgSrc"
        class="formatting-card-image"
        alt="展示图片"/>
      <template #footer>
        <el-space :size="60">
          <el-button class="formatting-card-button" type="info" text @click="onPreview">预览</el-button>
          <el-button class="formatting-card-button" type="primary" text @click="onUse">使用</el-button>
        </el-space>
      </template>
    </el-card>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: "FormattingCard",
  props: {
    cardId:{
      type:String,
      required:true,
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
    const onPreview = () => {
      context.emit('previewEvent');
    };

    const onUse = () => {
      context.emit('useFormatEvent', props.cardId);
    };

    return {
      onPreview,
      onUse
    };
  }
});
</script>

<style scoped lang="scss">
.formatting-card-container {
  width: 18rem;
  height: 16rem;
}
.formatting-card-card {
  width: 100%;
  height: 100%;
}
.el-card :deep .el-card__header {
  height: 2rem !important;
  padding: 0 !important;
}

.el-card :deep .el-card__body {
  width: 100%;
  height: 75%;
  padding: 0 !important;
}

.el-card :deep .el-card__footer {
  height: 2rem !important;
  padding: 0 !important;
}

.formatting-card-image {
  width: 100%;
  height: 100%;
}

.formatting-card-button {
  margin-top: 0.25rem;
  width: 4rem !important;
  height: 1.5rem !important;
}
</style>
