<template>
  <div v-if="items.length > 0" class="toc--list">
    <div v-for="item in items" :key="item.id" class="toc--item" :class="'toc--item--level_' + item.level">
      <a
        :href="'#' + item.id"
        :style="{
        display: 'block',
        // backgroundColor: item.isActive ? '#d3dce6' : 'transparent',
        // color: item.isScrolledOver ? '#888' : '#000',
        borderRadius: '4px' }"
        @click.prevent="onItemClick(item.id)"
      >
        {{ item.text }}
      </a>
    </div>
  </div>
  <div v-else class="toc--empty_state">
    <p>试试在文档中设置一个标题吧</p>
  </div>
</template>

<script>
import { TextSelection } from '@tiptap/pm/state'

export default {
  props: {
    items: {
      type: Array,
      required: true,
    },
    editor: {
      type: Object,
      required: true,
    },
  },
  methods: {
    onItemClick(id) {
      if (!this.editor) return

      const element = this.editor.view.dom.querySelector(`[data-toc-id="${id}"]`)
      if (!element) return

      const pos = this.editor.view.posAtDOM(element, 0)
      const tr = this.editor.view.state.tr
      tr.setSelection(new TextSelection(tr.doc.resolve(pos)))
      this.editor.view.dispatch(tr)
      this.editor.view.focus()

      if (history.pushState) {
        history.pushState(null, null, `#${id}`)
      }

      // Scroll to the editor content container
      const editorContainer = document.querySelector('.editor-content')
      if (editorContainer) {
        editorContainer.scrollTo({
          top: element.offsetTop,
          behavior: 'smooth',
        })
      }
    },
  },
}
</script>

<style>
.toc--empty_state {
  display: flex;
  justify-content: center;
}

.toc--empty_state p {
  text-align: center;
  color: #afafaf;
}
</style>