<template>
  <div id="mind-map-container" style="width:100%;"></div>
</template>

<script lang="ts">
import {defineComponent, nextTick, onMounted} from 'vue';
import Export from 'simple-mind-map/src/plugins/Export.js'
import MindMap from 'simple-mind-map';
import { themeList } from 'simple-mind-map/src/constants/constant'

export default defineComponent({
  name: 'MindMapPanel',
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  setup() {
    let AIMindMap: MindMap | null = null;
    // 定义思维导图的初始数据
    const mindMapData = {
      "data": {
        "text": "智能思维导图"
      },
      "children": [
        {
          "data":{
            "text": "智能生成"
          },
          "children": [
            {
              "data": {
                "text": "自动总结文章要点，生成思维导图",
              },
              "children": []
            },
          ]
        },
        {
          "data":{
            "text": "导出为PNG"
          },
          "children": [
            {
              "data": {
                "text": "导出思维导图为PNG格式",
              },
              "children": []
            },
          ]
        },
        {
          "data":{
            "text": "切换主题"
          },
          "children": [
            {
              "data": {
                "text": "切换思维导图主题样式",
              },
              "children": []
            },
          ]
        }
      ]
    };


    const drawMindMap = async () => {
      await nextTick();
      const container = document.getElementById('mind-map-container') as HTMLElement;
      const exportPadding = 75;
      console.log(typeof exportPadding)
      if (container) {
        AIMindMap = new MindMap({
          el: container,
          data: mindMapData,
          readonly: true,
          layout: "mindMap",
          theme: 'default',
          fit:true,
          exportPaddingX: exportPadding,
          exportPaddingY: exportPadding,
        } as any);
      }
    };

    onMounted(drawMindMap);

    MindMap.usePlugin(Export)

    const setMindMapData = (mindMapData) => {
      if (AIMindMap) {
        AIMindMap.setData(mindMapData);
      }
    };

    const exportMindMapData = () => {
      if (AIMindMap) {
        const mindMapData = AIMindMap.getData(false);
        AIMindMap.export('png', true, mindMapData.data.text)
      } else {
        console.error('Mind map instance is not initialized.');
      }
    };
    const setMindMapTheme = (themeValue) => {
      if (AIMindMap) {
        console.log(themeList)
        AIMindMap.setTheme(themeValue)
      } else {
        console.error('Mind map instance is not initialized.');
      }
    };

    return {
      mindMapData,
      setMindMapData,
      exportMindMapData,
      setMindMapTheme,
    };
  },
});
</script>

<style scoped lang="scss">
#mind-map-container {
  width: 100%;
  height: 60vh;
  background-color: #f0f0f0;
}

</style>
