<template>
  <div v-if="items.length > 0" class="toc--list">
    <div v-for="item in items" :key="item.id" class="toc--item" :class="'toc--item--level_' + item.level">
      <a
        :href="'#' + item.id"
        :style="{ display: 'block', backgroundColor: item.isActive ? 'rgba(0, 0, 0, .05)' : 'transparent', color: item.isScrolledOver && !item.isActive ? '#888' : '#000', borderRadius: '4px' }"
        @click.prevent="onItemClick(item.id)"
      >
        {{ item.text }}
      </a>
    </div>
  </div>
  <div v-else class="toc--empty_state">
    <p>Start editing your document to see the outline.</p>
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
