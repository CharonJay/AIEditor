<template>
  <div class="option-drawer-div">
    <el-drawer
        class="option-drawer"
        size="75%"
        title="预览界面"
        v-model="drawerVisible"
        @close="drawerVisible = false"
        direction="rtl">
      <format-editor-panel
        @useFormatEventPreview="onUse"
        ref="formatEditorPanel"
        :card-id="selectedId"
        :initial-content="selectedContent"
        :card-title="selectedCardTitle"
        :img-src="selectedImgSrc">
      </format-editor-panel>
    </el-drawer>
    <el-space wrap :size="20">
      <formatting-card
        v-for="(card, index) in cards"
        :key="index"
        :card-id="String(card.id)"
        :card-title="card.name"
        :img-src="card.image_path"
        :is-delete-visible="true"
        @previewEvent="showDrawer(card)"
        @useFormatEvent="onUse"
        @deleteCardEvent="deleteCard"
      >
      </formatting-card>
    </el-space>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import FormattingCard from "@/components/editor/FormattingCard.vue";
import FormatEditorPanel from "@/components/editor/FormatEditorPanel.vue"
import axios from "axios";
import {ElMessage} from "element-plus";

export default defineComponent({
  name: 'UserFormat',
  components:{
    FormatEditorPanel,
    FormattingCard
  },
  props: {
    // 定义组件的 props
    propA: String,
  },
  setup(props, context) {
    const propAValue = ref(props.propA); // 使用 props 中的属性,仅用于避免props报错
    propAValue.value = "测试"
    const drawerVisible = ref(false);
    const cards = ref<any[]>([]); // 假设 cards 是一个 ref 数组，类型为 any[]
    const selectedId = ref('');
    const selectedContent = ref('');
    const selectedCardTitle = ref('');
    const selectedImgSrc = ref('');
    const formatEditorPanel = ref<any>(null); // 假设 formatEditorPanel 是一个 ref 对象，类型为 any

    const username = localStorage.getItem("username")
    const fetchCards = async () => {
      try {
        const response = await axios.get(`/api/user/template/?username=${username}`);
        cards.value = response.data;
      } catch (error) {
        console.error("Failed to fetch cards data:", error);
      }
    };
    const showDrawer = (card) => {
      selectedContent.value = card.content;
      selectedId.value = String(card.id);
      selectedCardTitle.value = card.name;
      selectedImgSrc.value = card.image_path;
      drawerVisible.value = true;
      // 检查 formatEditorPanel 是否存在
      if (formatEditorPanel.value) {
        formatEditorPanel.value.updateContent(card.content);
      } else {
        console.error("formatEditorPanel is not initialized.");
      }
    };

    const onUse = (cardId: string) => {
      drawerVisible.value = false
      context.emit('useFormat', cardId);
    };

    const deleteCard = async (cardId: string) => {
      try {
        await axios.delete(`/api/user/template/${cardId}/`);
        ElMessage.success("模板删除成功！")
        // 更新界面
        const index = cards.value!.findIndex(card => String(card.id) === cardId);
        if (index !== -1) {
          cards.value.splice(index, 1); // 从 cards 数组中移除已删除的卡片
        }
      } catch (error) {
        ElMessage.error("模板删除失败！")
      }
    };

    onMounted(fetchCards);
    return {
      drawerVisible,
      cards,
      selectedId,
      selectedContent,
      selectedCardTitle,
      formatEditorPanel,
      selectedImgSrc,
      showDrawer,
      onUse,
      deleteCard
    };
  }

});
</script>

<style scoped>
.option-drawer-div :deep .el-overlay{
  position: absolute;
}
.option-drawer{
  position: absolute;
}
.formatEmpty{
  width: 100%;
}
</style>
