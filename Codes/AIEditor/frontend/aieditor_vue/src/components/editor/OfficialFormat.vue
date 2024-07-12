<template>
  <div class="option-drawer-div">
    <el-drawer
        class="option-drawer"
        size="75%"
        title="预览界面"
        v-model="templateDrawerVisible"
        @close="templateDrawerVisible = false"
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
        @previewEvent="showDrawer(card)"
        @useFormatEvent="onUse" >
      </formatting-card>
    </el-space>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref} from 'vue';
import FormattingCard from "./FormattingCard.vue";
import FormatEditorPanel from "./FormatEditorPanel.vue"
import axios from "axios";

export default defineComponent({
  name: 'OfficialFormat',
  components: {
    FormattingCard,
    FormatEditorPanel
  },
  setup(props, context)  {
    const templateDrawerVisible = ref(false);
    const cards = ref([]);
    const selectedId = ref('');
    const selectedContent = ref('');
    const selectedCardTitle = ref('');
    const selectedImgSrc = ref('');
    const formatEditorPanel = ref(null);

    const username = "官方模板管理用户"

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
      templateDrawerVisible.value = true;
      formatEditorPanel.value.updateContent(card.content);
    };

    const onUse = (cardId: string) => {
      templateDrawerVisible.value = false
      context.emit('useFormat', cardId);
    };

    onMounted(fetchCards);

    return {
      templateDrawerVisible,
      cards,
      selectedId,
      selectedContent,
      selectedCardTitle,
      selectedImgSrc,
      formatEditorPanel,
      showDrawer,
      onUse
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

</style>
