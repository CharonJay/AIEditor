<template>
  <div>
    <template v-for="(item, index) in items" :key="index">
      <el-divider v-if="item.type === 'divider'" :key="`divider${index}`" direction="vertical" />
      <menu-button-dropdown-item v-else-if="item.type === 'buttonDropdown'" :key="`buttonDropdown${index}` " v-bind="item"/>
      <menu-option-item v-else-if="item.type === 'selector'" :key="`selector${index}`" v-model="selectedValues[index]" v-bind="item"/>
      <menu-button-item v-else :key="index" v-bind="item" />
    </template>
  </div>
</template>

<script>
import MenuButtonItem from './MenuButtonItem.vue';
import MenuOptionItem from "./MenuOptionItem.vue";
import MenuButtonDropdownItem from "./MenuButtonDropdownItem.vue";
import {reactive} from "vue";

export default {
  components: {
    MenuButtonItem,
    MenuOptionItem,
    MenuButtonDropdownItem
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
      },
      {
        icon: 'underline',
        title: 'Underline',
        action: () => props.editor.chain().focus().toggleUnderline().run(),
      },
      {
        icon: 'italic',
        title: 'Italic',
        action: () => props.editor.chain().focus().toggleItalic().run(),
      },
      {
        icon: 'strikethrough',
        title: 'Strike',
        action: () => props.editor.chain().focus().toggleStrike().run(),
      },
      {
        icon: 'code-view',
        title: 'Code',
        action: () => props.editor.chain().focus().toggleCode().run(),
      },
      {
        icon: 'mark-pen-line',
        title: 'Highlight',
        action: () => props.editor.chain().focus().toggleHighlight().run(),
      },
      {
        type: 'divider'
      },
      {
        icon: 'align-left',
        title: 'AlignLeft',
        action: () => props.editor.chain().focus().setTextAlign('left').run(),
      },
      {
        icon: 'align-center',
        title: 'AlignCenter',
        action: () => props.editor.chain().focus().setTextAlign('center').run(),
      },
      {
        icon: 'align-right',
        title: 'AlignRight',
        action: () => props.editor.chain().focus().setTextAlign('right').run(),
      },
      {
        icon: 'align-justify',
        title: 'AlignJustify',
        action: () => props.editor.chain().focus().setTextAlign('justify').run(),
      },
      {
        type: 'divider'
      },
      {
        type: 'buttonDropdown',
        icon: 'heading',
        title: 'heading',
        options: [
          {
            label: 'h1',
            value: '1',
          },
          {
            label: 'h2',
            value: '2',
          },
          {
            label: 'h3',
            value: '3',
          },
          {
            label: 'h4',
            value: '4',
          },
          {
            label: 'h5',
            value: '5',
          },
          {
            label: 'h6',
            value: '6',
          }
        ],
        action: (value) => props.editor.chain().focus().toggleHeading({ level: parseInt(value) }).run(),
      },
      {
        type: 'buttonDropdown',
        icon: 'font-family',
        title: 'font-family',
        options: [
          {
            label: 'Inter',
            value: 'Inter',
          },
          {
            label: 'Comic Sans',
            value: 'Comic Sans',
          },
          {
            label: 'serif',
            value: 'serif',
          },
          {
            label: 'monospace',
            value: 'monospace',
          },
          {
            label: 'SimHei',
            value: 'SimHei',
          },
          {
            label: 'Microsoft Yahei',
            value: 'Microsoft Yahei',
          },
          {
            label: 'Microsoft JhengHei',
            value: 'Microsoft JhengHei',
          },
          {
            label: 'KaiTi',
            value: 'KaiTi',
          },
        ],
        action: (value) => props.editor.chain().focus().setFontFamily(value).run(),
      },
      {
        type: 'buttonDropdown',
        icon: 'font-size',
        title: 'font-family',
        options: [
          {
            label: '10pt',
            value: '10pt',
          },
          {
            label: '12pt',
            value: '12pt',
          },
          {
            label: '14pt',
            value: '14pt',
          },
          {
            label: '16pt',
            value: '16pt',
          },
          {
            label: '18pt',
            value: '18pt',
          },
        ],
        action: (value) => props.editor.chain().focus().setFontSize(value).run(),
      },
      {
        icon: 'paragraph',
        title: 'Paragraph',
        action: () => props.editor.chain().focus().setParagraph().run(),
      },
      {
        icon: 'list-unordered',
        title: 'Bullet List',
        action: () => props.editor.chain().focus().toggleBulletList().run(),
      },
      {
        icon: 'list-ordered',
        title: 'Ordered List',
        action: () => props.editor.chain().focus().toggleOrderedList().run(),
      },
      {
        icon: 'list-check-2',
        title: 'Task List',
        action: () => props.editor.chain().focus().toggleTaskList().run(),
      },
      {
        icon: 'code-box-line',
        title: 'Code Block',
        action: () => props.editor.chain().focus().toggleCodeBlock().run(),
      },
      {
        type: 'divider'
      },
      {
        icon: 'double-quotes-l',
        title: 'Blockquote',
        action: () => props.editor.chain().focus().toggleBlockquote().run(),
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
    const selectedValues = reactive({});  //selector更新文本所需

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
