<template>
    <div class="editor" v-if="editor" :style="{width}">
        <MenuBar class="editor-header" :editor="editor" />
        <editor-content class="editor-content" :editor="editor" />
    </div>
</template>

<script>
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import MenuBar from './MenuBar.vue'

export default {
  components: {
    EditorContent,
    MenuBar
  },
  props: {
    width: {
      type: String,
      default: '800px'
    }
  },
  setup() {
    const editor = useEditor({
      content: '<p>I’m running Tiptap with vue-next. 🎉</p>',
      extensions: [
        StarterKit
      ]
    })
    return {
      editor
    }
  }
}
</script>