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
        <el-aside class="left-aside">
          left_Aside
        </el-aside>
        <el-main class="main">
          <div class="editor-main" v-if="editor">
            <editor-content class="editor-content" :editor="editor" />
          </div>
        </el-main>
        <el-aside class="aside right-aside">
          right_Aside
        </el-aside>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ArrowLeft } from '@element-plus/icons-vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Highlight from '@tiptap/extension-highlight'
import TaskList from "@tiptap/extension-task-list";
import TaskItem from "@tiptap/extension-task-item";
import TextAlign from '@tiptap/extension-text-align'
import FontFamily from "@tiptap/extension-font-family";
import TextStyle from "@tiptap/extension-text-style";
import FontSize from "tiptap-extension-font-size";
import MenuBar from './MenuBar.vue'

export default {
  name: 'EditorPanel',
  components: {
    EditorContent,
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
  setup() {
    const editor = useEditor({
      content: '<p>I’m running Tiptap with vue-next. 🎉</p>',
      extensions: [
        Highlight,
        TaskList,
        TaskItem,
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
        StarterKit
      ]
    })
    return {
      editor
    }
  }
}
</script>

<style>
  .page-header{
    height: 60px;
  }
  .breadcrumb-header{

  }
  .parent-container{
    height: 860px;
    width: 1640px;
  }
  .header-menu {
    position: relative;
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  .left-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 50px;
     width:15vw;
  }
  .right-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 45px;
     width:15vw;
  }
  .main {
    background-color: #E9EEF3;
    color: #333;
    line-height: 20px;
    text-align: left;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .editor-menu {
    display: flex;
    flex-direction: column;
    max-height: 47rem;
    color: #0d0d0d;
    background-color: #fff;
    border: 3px solid #0a0303;
    border-radius: .75rem;
  }

  .editor-main {
    display: flex;
    flex-direction: column;
    height: 47rem;
    max-height: 47rem;
    color: #0d0d0d;
    background-color: #fff;
    border: 3px solid #0a0303;
    border-radius: .5rem;
  }

  .editor-content {
    padding: .7rem .5rem;
    background: #ffffff;
    border-radius: 5px;
    height: 100%;
    max-width: 100%;
    overflow-wrap: break-word; /* Ensure long words break and wrap */
    overflow-x: hidden;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
  .ProseMirror:focus {
  outline: 0;
  }
</style>