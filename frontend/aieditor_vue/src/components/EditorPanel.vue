<template>
  <el-page-header class="page-header" :icon="ArrowLeft">
    <template #breadcrumb>
      <el-breadcrumb class="breadcrumb-header" separator="/">
        <el-breadcrumb-item :to="{ path: './page-header.html' }">
          homepage
        </el-breadcrumb-item>
        <el-breadcrumb-item>
          <a href="./page-header.html">route 1</a></el-breadcrumb-item>
        <el-breadcrumb-item>route 2</el-breadcrumb-item>
      </el-breadcrumb>
    </template>
    <template #content>
      <span class="text-large font-600 mr-3"> Title </span>
    </template>
  </el-page-header>
  <div class="common-layout">
    <el-container class="parent-container">
      <el-header class="header-menu">
        <div class="editor-menu" v-if="editor">
          <MenuBar class="editor-header" :editor="editor" />
        </div>
      </el-header>
      <el-container>
        <el-aside  class="left-aside sidebar">
          <TocPanel :items="toc" :editor="editor"/>
        </el-aside>
        <el-main class="main">
          <div class="editor-main" v-if="editor">
            <editor-content class="editor-content" :editor="editor" />
            <div class="character-count" v-if="editor">
              {{ editor.storage.characterCount.characters() }} characters
            </div>
          </div>
        </el-main>
        <el-aside class="aside right-aside">
          <chat-box></chat-box>
        </el-aside>
      </el-container>
    </el-container>
  </div>
</template>

<script>

import {ArrowLeft} from "@element-plus/icons-vue";
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Highlight from '@tiptap/extension-highlight'
import TaskList from "@tiptap/extension-task-list";
import TaskItem from "@tiptap/extension-task-item";
import TextAlign from '@tiptap/extension-text-align'
import FontFamily from "@tiptap/extension-font-family";
import TextStyle from "@tiptap/extension-text-style";
import Underline from "@tiptap/extension-underline";
import CharacterCount from "@tiptap/extension-character-count";
import Mathematics from '@tiptap-pro/extension-mathematics'
import {getHierarchicalIndexes, TableOfContents} from "@tiptap-pro/extension-table-of-contents";
import FontSize from "tiptap-extension-font-size";
import Placeholder from '@tiptap/extension-placeholder'

import MenuBar from './MenuBar.vue'
import ChatBox from './Chat.vue'; // 确保路径正确

import {ref} from "vue";
import TocPanel from "./TocPanel.vue";

import 'katex/dist/katex.min.css';
import '../assets/EditorPanel.css';
import '../assets/TiptapStyle.css';


export default {
  name: 'EditorPanel',
  components: {
    EditorContent,
    TocPanel,
    ChatBox,
    MenuBar
  },
  computed: {
    ArrowLeft() {
      return ArrowLeft
    }
  },
  props: {
    msg: String
  },
  data() {
    return {
      panelVisible: false // 控制面板显示状态的变量
    };
  },
  methods: {
    togglePanel() {
      this.panelVisible = !this.panelVisible; // 切换面板显示状态
    }
  },
  setup() {
    const toc = ref([])
    const editor = useEditor({
      content:
          '<h1> 现在支持目录大纲了 </h1>'+
          '<h2> 二级标题 </h2>'+
          '<h3> 三级标题 </h3>'+
          '<h4> 四级标题 </h4>'+
          '<h1> 一级标题 </h1>'+
          '<h5> 五级标题 </h5>'+
          '<h6> 六级标题 </h6>'+
          '<p>I’m running Tiptap with vue-next. 🎉   </p>' +
          '<li>现在支持字符统计了</li>' +
          '<li>现在支持 $\\LaTeX$ 语法了</li>' +
          '<p>------------分隔符------------------</p>'+
          '<p>缺失的功能:</p>'+
          '<li>表格插入</li>'+
          '<li>图片插入</li>'+
          '<li>字体颜色修改</li>',

      extensions: [
        Highlight,
        TaskItem.configure({
          nested: true,
        }),
        TextStyle,
        TaskList.configure({
          itemTypeName: 'taskItem',
        }),
        FontSize.configure({
          types: ['textStyle'],
        }),
        TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
        FontFamily.configure({
          types: ['textStyle'],
        }),
        Underline.configure({
          HTMLAttributes: {
            class: 'my-custom-class',
          },
        }),
        CharacterCount.configure({
            mode: 'textSize',
        }),
        Mathematics,
        TableOfContents.configure({
          getIndex: getHierarchicalIndexes,
          onUpdate(content) {
            toc.value = content.map(item => ({
              id: item.id,
              text: item.textContent,
              level: item.level,
              isActive: item.isActive,
              isScrolledOver: item.isScrolledOver,
            }));
          },
        }),
        Placeholder.configure({
          placeholder: 'Write something …',
        }),
        StarterKit,
      ]
    })
    return {
      editor,
      toc
    }
  }
}


</script>
