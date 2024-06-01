<template>
  <div>
    <template v-for="(item, index) in items" :key="index">
      <el-divider v-if="item.type === 'divider'" :key="`divider${index}`" direction="vertical" />
      <menu-option-item v-else-if="item.type === 'selector'" :key="`selector${index}`" v-model="selectedValues[index]" v-bind="item"/>
      <menu-button-item v-else :key="index" v-bind="item" />
    </template>
  </div>
</template>

<script>
import MenuButtonItem from './MenuButtonItem.vue';
import MenuOptionItem from "@/components/MenuOptionItem.vue";
import {reactive, ref} from "vue";

export default {
  components: {
    MenuButtonItem,
    MenuOptionItem
  },

  props: {
    editor: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const items = reactive([
      {
        icon: 'arrow-go-back-line',
        title: 'Undo',
        action: () => props.editor.chain().focus().undo().run()
      },
      {
        icon: 'arrow-go-forward-line',
        title: 'Redo',
        action: () => props.editor.chain().focus().redo().run()
      },
      {
        type: 'divider'
      },
      {
        icon: 'bold',
        title: 'Bold',
        action: () => props.editor.chain().focus().toggleBold().run(),
        isActive: () => props.editor.isActive('bold')
      },
      {
        icon: 'italic',
        title: 'Italic',
        action: () => props.editor.chain().focus().toggleItalic().run(),
        isActive: () => props.editor.isActive('italic')
      },
      {
        icon: 'strikethrough',
        title: 'Strike',
        action: () => props.editor.chain().focus().toggleStrike().run(),
        isActive: () => props.editor.isActive('strike')
      },
      {
        icon: 'code-view',
        title: 'Code',
        action: () => props.editor.chain().focus().toggleCode().run(),
        isActive: () => props.editor.isActive('code')
      },
      {
        icon: 'mark-pen-line',
        title: 'Highlight',
        action: () => props.editor.chain().focus().toggleHighlight().run(),
        isActive: () => props.editor.isActive('highlight')
      },
      {
        type: 'divider'
      },
      {
        icon: 'align-left',
        title: 'AlignLeft',
        action: () => props.editor.chain().focus().setTextAlign('left').run(),
        isActive: () => props.editor.isActive({textAlign: 'left'})
      },
      {
        icon: 'align-center',
        title: 'AlignCenter',
        action: () => props.editor.chain().focus().setTextAlign('center').run(),
        isActive: () => props.editor.isActive({textAlign: 'center'})
      },
      {
        icon: 'align-right',
        title: 'AlignRight',
        action: () => props.editor.chain().focus().setTextAlign('right').run(),
        isActive: () => props.editor.isActive({textAlign: 'right'})
      },
      {
        icon: 'align-justify',
        title: 'AlignJustify',
        action: () => props.editor.chain().focus().setTextAlign('justify').run(),
        isActive: () => props.editor.isActive({textAlign: 'justify'})
      },
      {
        type: 'divider'
      },
      {
        type: 'selector',
        icon: 'align-justify',
        options: [
          {
            label: 'Heading 1',
            value: 'h1',
            title: 'Heading 1',
            action: () => props.editor.chain().focus().toggleHeading({level: 1}).run(),
            isActive: () => props.editor.isActive('heading', {level: 1})
          },
          {
            label: 'Heading 2',
            value: 'h2',
            title: 'Heading 2',
            action: () => props.editor.chain().focus().toggleHeading({level: 2}).run(),
            isActive: () => props.editor.isActive('heading', {level: 2})
          },
          {
            label: 'Heading 3',
            value: 'h3',
            title: 'Heading 3',
            action: () => props.editor.chain().focus().toggleHeading({level: 3}).run(),
            isActive: () => props.editor.isActive('heading', {level: 3})
          },
          {
            label: 'Heading 4',
            value: 'h4',
            title: 'Heading 4',
            action: () => props.editor.chain().focus().toggleHeading({level: 4}).run(),
            isActive: () => props.editor.isActive('heading', {level: 4})
          },
          {
            label: 'Heading 5',
            value: 'h5',
            title: 'Heading 5',
            action: () => props.editor.chain().focus().toggleHeading({level: 5}).run(),
            isActive: () => props.editor.isActive('heading', {level: 5})
          },
          {
            label: 'Heading 6',
            value: 'h6',
            title: 'Heading 6',
            action: () => props.editor.chain().focus().toggleHeading({level: 6}).run(),
            isActive: () => props.editor.isActive('heading', {level: 6})
          }
        ]
      },
      {
        type: 'selector',
        options: [
          {
            label: 'Inter',
            value: 'Inter',
            title: 'Inter',
            action: () => props.editor.chain().focus().setFontFamily('Inter').run(),
            isActive: () => props.editor.isActive('textStyle', {fontFamily: 'Inter'})
          },
          {
            label: 'Comic Sans',
            value: 'Comic Sans',
            title: 'Comic Sans',
            action: () => props.editor.chain().focus().setFontFamily('Comic Sans MS, Comic Sans').run(),
            isActive: () => props.editor.isActive('textStyle', {fontFamily: 'Comic Sans MS, Comic Sans'})
          },
          {
            label: 'serif',
            value: 'serif',
            title: 'serif',
            action: () => props.editor.chain().focus().setFontFamily('serif').run(),
            isActive: () => props.editor.isActive('textStyle', {fontFamily: 'serif'})
          },
          {
            label: 'monospace',
            value: 'monospace',
            title: 'monospace',
            action: () => props.editor.chain().focus().setFontFamily('monospace').run(),
            isActive: () => props.editor.isActive('textStyle', {fontFamily: 'monospace'})
          },
          {
            label: 'cursive',
            value: 'cursive',
            title: 'cursive',
            action: () => props.editor.chain().focus().setFontFamily('cursive').run(),
            isActive: () => props.editor.isActive('textStyle', {fontFamily: 'cursive'})
          }
        ]
      },
      {
        type: 'selector',
        options: [
          {
            label: '10pt',
            value: '10pt',
            title: '10pt',
            action: () => props.editor.chain().focus().setFontSize('10pt').run(),
            isActive: () => props.editor.isActive('textStyle', {fontSize: '10pt'})
          },
          {
            label: '12pt',
            value: '12pt',
            title: '12pt',
            action: () => props.editor.chain().focus().setFontSize('12pt').run(),
            isActive: () => props.editor.isActive('textStyle', {fontSize: '12pt'})
          },
          {
            label: '14pt',
            value: '14pt',
            title: '14pt',
            action: () => props.editor.chain().focus().setFontSize('14pt').run(),
            isActive: () => props.editor.isActive('textStyle', {fontSize: '14pt'})
          },
          {
            label: '16pt',
            value: '16pt',
            title: '16pt',
            action: () => props.editor.chain().focus().setFontSize('16pt').run(),
            isActive: () => props.editor.isActive('textStyle', {fontSize: '16pt'})
          },
          {
            label: '18pt',
            value: '18pt',
            title: '18pt',
            action: () => props.editor.chain().focus().setFontSize('18pt').run(),
            isActive: () => props.editor.isActive('textStyle', {fontSize: '18pt'})
          }
        ]
      },
      {
        icon: 'paragraph',
        title: 'Paragraph',
        action: () => props.editor.chain().focus().setParagraph().run(),
        isActive: () => props.editor.isActive('paragraph')
      },
      {
        icon: 'list-unordered',
        title: 'Bullet List',
        action: () => props.editor.chain().focus().toggleBulletList().run(),
        isActive: () => props.editor.isActive('bulletList')
      },
      {
        icon: 'list-ordered',
        title: 'Ordered List',
        action: () => props.editor.chain().focus().toggleOrderedList().run(),
        isActive: () => props.editor.isActive('orderedList')
      },
      {
        icon: 'list-check-2',
        title: 'Task List',
        action: () => props.editor.chain().focus().toggleTaskList().run(),
        isActive: () => props.editor.isActive('taskList')
      },
      {
        icon: 'code-box-line',
        title: 'Code Block',
        action: () => props.editor.chain().focus().toggleCodeBlock().run(),
        isActive: () => props.editor.isActive('codeBlock')
      },
      {
        type: 'divider'
      },
      {
        icon: 'double-quotes-l',
        title: 'Blockquote',
        action: () => props.editor.chain().focus().toggleBlockquote().run(),
        isActive: () => props.editor.isActive('blockquote')
      },
      {
        icon: 'separator',
        title: 'Horizontal Rule',
        action: () => props.editor.chain().focus().setHorizontalRule().run()
      },
      {
        type: 'divider'
      },
      {
        icon: 'text-wrap',
        title: 'Hard Break',
        action: () => props.editor.chain().focus().setHardBreak().run()
      },
      {
        icon: 'format-clear',
        title: 'Clear Format',
        action: () => props.editor.chain()
            .focus()
            .clearNodes()
            .unsetAllMarks()
            .run()
      }
    ]);
    const selectedValues = reactive({});

    return {
      items,
      selectedValues,
    };
  }
};
</script>

<style lang="scss">
.el-divider {
  margin-left: 0.75rem;
  margin-right: 0.75rem;
  background-color: rgba(10, 3, 3, 0.6);
  height: 1.25rem;
  border-left: 0.1rem solid rgba(10, 3, 3, 0.49);
}
</style>
