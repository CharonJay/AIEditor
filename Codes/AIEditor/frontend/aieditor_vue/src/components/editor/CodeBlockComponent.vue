<template>
  <node-view-wrapper class="code-block">
    <el-select
        v-model="selectedLanguage"
        clearable placeholder="auto"
        class="language-select"
        size="small"
    >
      <el-option
        v-for="(language, index) in languages"
        :key="index"
        :label="language"
        :value="language"
      ></el-option>
    </el-select>
    <pre><code><node-view-content/></code></pre>
  </node-view-wrapper>
</template>


<script>
import { NodeViewContent, nodeViewProps, NodeViewWrapper } from '@tiptap/vue-3'
import { ElSelect, ElOption } from 'element-plus'

export default {
  components: {
    NodeViewWrapper,
    NodeViewContent,
    ElSelect,
    ElOption,
  },

  props: nodeViewProps,
  data() {
    return {
      languages: this.extension.options.lowlight.listLanguages(),
    }
  },
  computed: {
    selectedLanguage: {
      get() {
        return this.node.attrs.language
      },
      set(language) {
        this.updateAttributes({ language })
      },
    },
  },
}
</script>


<style lang="scss">
.tiptap {
  .code-block {
    position: relative;

    .language-select {
      position: absolute;
      background-color: #ffffff;
      right: 0.5rem;
      top: 0.5rem;
      width: 5rem;
      border-radius: 8px;
    }
  }
}
</style>