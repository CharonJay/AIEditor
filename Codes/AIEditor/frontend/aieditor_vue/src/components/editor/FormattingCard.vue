<template>
  <el-container class="formatting-card-container">
    <el-card class="formatting-card-card" shadow="hover">
      <template #header>
        <div v-if="isDeleteVisible" class="formatting-card-header">
          <span class="formatting-card-title">{{ cardTitle }}</span>
          <el-button  class="formatting-card-delete-button" @click="handleDeleteCard">
            <i class="ri-delete-bin-line"></i>
          </el-button>
        </div>
        <div v-if="!isDeleteVisible">
          {{ cardTitle }}
        </div>
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
import '../../assets/remixicon/remixicon.css'
import {ElMessage, ElMessageBox, ElMessageBoxOptions} from "element-plus";

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
    },
    isDeleteVisible:{
      type: Boolean,
      default: true, // 默认显示删除按钮，如果不需要始终显示可以设置为 false
      required:true
    }
  },
  setup(props, context) {
    const onPreview = () => {
      context.emit('previewEvent');
    };

    const onUse = () => {
      context.emit('useFormatEvent', props.cardId);
    };

    const handleDeleteCard = () => {
      const options: ElMessageBoxOptions = {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      };

      ElMessageBox.confirm('此操作将永久删除该卡片, 是否继续?', '提示', options)
      .then(() => {
        context.emit('deleteCardEvent', props.cardId);
      })
      .catch(() => {
        ElMessage.info('取消删除操作');
      });
    };

    return {
      onPreview,
      onUse,
      handleDeleteCard
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
.formatting-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
.formatting-card-title {
  flex-grow: 1;
  text-align: center;
  margin-left: 2.5rem;
}

.formatting-card-button {
  margin-top: 0.25rem;
  width: 4rem !important;
  height: 1.5rem !important;
}
.formatting-card-delete-button {
  border: none;
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 1rem;
}
</style>
