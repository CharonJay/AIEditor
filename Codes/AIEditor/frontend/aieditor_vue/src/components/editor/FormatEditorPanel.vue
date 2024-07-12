<template>
  <el-container class="format-editor-panel-info">
      <el-aside width="200px">
        <img
        :src="imgSrc"
        class="formatting-editor-panel-image"
        alt="预览图片"/>
      </el-aside>
      <el-main>
        <el-row class="format-editor-panel-row-1">
            <el-text class="format-editor-panel-title">{{cardTitle}}</el-text>
        </el-row>
        <el-row class="format-editor-panel-row-2">
            <el-button class="format-editor-panel-button" @click="onUse">使用</el-button>
        </el-row>
      </el-main>
  </el-container>
  <el-divider class="format-editor-panel-divider"></el-divider>
  <el-container class="format-editor-panel-editor">
    <el-main>
      <editor-content class="format-editor-content" :editor="<Editor>formatEditor" />
    </el-main>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Editor } from "@tiptap/vue-3";
import {EditorContent, useEditor, VueNodeViewRenderer} from "@tiptap/vue-3";
import Highlight from "@tiptap/extension-highlight";
import TaskList from "@tiptap/extension-task-list";
import TaskItem from "@tiptap/extension-task-item";
import TextStyle from "@tiptap/extension-text-style";
import FontSize from "tiptap-extension-font-size";
import TextAlign from "@tiptap/extension-text-align";
import FontFamily from "@tiptap/extension-font-family";
import Underline from "@tiptap/extension-underline";
import CharacterCount from "@tiptap/extension-character-count";
import Mathematics from "@tiptap-pro/extension-mathematics";
import {getHierarchicalIndexes, TableOfContents} from "@tiptap-pro/extension-table-of-contents";
import Placeholder from "@tiptap/extension-placeholder";
import StarterKit from "@tiptap/starter-kit";
import Image from "@tiptap/extension-image";
import Typography from "@tiptap/extension-typography";
import CodeBlockLowlight from "@tiptap/extension-code-block-lowlight";
import CodeBlockComponent from "./CodeBlockComponent.vue";
import {lowlight} from "lowlight/lib/core";
import Color from "@tiptap/extension-color";
import textEnhancements from "../../custom_extensions/textEnhancements";


import '../../assets/TiptapStyle.css';
export default defineComponent({
  name: "FormatEditorPanel",
  props: {
    cardId:{
      type:String,
      required:true,
    },
    initialContent: {
      type: String,
      required: true,
    },
    cardTitle: {
      type: String,
      required: true
    },
    imgSrc: {
      type: String,
      required: true
    }
  },
  computed: {
    Editor() {
      return Editor
    }
  },
  components: {
    EditorContent,
    Editor
  },

  emits: ['useFormatEventPreview'],
  setup(props, context){
    const formatEditor = useEditor({
      editable:false,
      content: props.initialContent,
      extensions: [
        Highlight,
        TaskList,
        TaskItem.configure({
          nested: true,
        }),
        TextStyle,
        FontSize.configure({
          types: ['textStyle'],
        }),
        TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
        FontFamily.configure({
          types: ['textStyle'],
        }),
        Underline,
        CharacterCount.configure({
            mode: 'textSize',
        }),
        Mathematics,
        Placeholder.configure({
          placeholder: 'Write something …',
        }),
        StarterKit,
        Image,
        Typography,
        CodeBlockLowlight.extend({
            addNodeView() {
              return VueNodeViewRenderer(CodeBlockComponent)
            },
        }).configure({ lowlight }),
        Color,
        textEnhancements,
      ]
    })
    const updateContent = (content: string) => {
      formatEditor.value.commands.clearContent();
      formatEditor.value.commands.insertContent(content);
    };
    const onUse = () => {
      context.emit('useFormatEventPreview', props.cardId);
    };
    return {
      formatEditor,
      updateContent,
      onUse
    }
  }
});
</script>

<style scoped lang="scss">
.el-main{
  padding-top: 0;
  padding-bottom: 0;
}
.el-aside{
  padding-top: 0;
  padding-bottom: 0;
}
.format-editor-panel-info{
  width: 100%;
  height: 9rem;
}
.formatting-editor-panel-image{
  width: 100%;
  height: 8rem;
}
.format-editor-panel-title {
  text-align: left;
  font-size: 16pt;
  width: 20rem;
}
.format-editor-panel-button{
  text-align: left;
  font-size: 12pt;
  width: 4rem;
}
.format-editor-panel-row-1{
  margin-top: 0;
}
.format-editor-panel-row-2{
  margin-top: 4rem;
}
.format-editor-panel-editor{
  width: 100%;
  max-height: 25rem;
  text-align: left;
}
.format-editor-content{
  width: 100%;
}
.format-editor-panel-divider{
  margin-top: 0;
  margin-bottom: 10px;
}
</style>
