<template>
  <el-page-header class="page-header" @back="goBack" :icon="ArrowLeft">
    <template #content>
      <el-space wrap :size="20">
        <el-text class="title-text">{{titleText}}</el-text>
        <el-dropdown trigger="click" class="header-dropdown-menu-file">
          <span class="el-dropdown-link">
            文件菜单
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="saveDocument">保存文档</el-dropdown-item>
              <el-dropdown-item @click="saveFormat">保存为模板</el-dropdown-item>
              <el-dropdown-item>
                <el-dropdown trigger="hover" placement="right-start" class="el-dropdown-state">
                  <span>
                    编辑状态
                    <el-icon  class="el-icon--right"><ArrowRight /></el-icon>
                  </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="changeFileStateTrue">允许编辑</el-dropdown-item>
                      <el-dropdown-item @click="changeFileStateFalse">只读</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </el-dropdown-item>
              <el-dropdown-item @click="openKnowledgeRepositoryDrawer">管理个人知识库</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-text class="file-state" :type="fileStateType">{{fileState}}</el-text>
        <el-text class="save-time">{{saveTime}}</el-text>
      </el-space>
    </template>
  </el-page-header>
  <el-container class="body">
    <div class="common-layout">
      <el-container v-loading.fullscreen.lock="loading" element-loading-text="AI正在努力中..." class="parent-container">
        <el-dialog class="ai-enhancement-dialog" v-model="dialogVisible" :title="dialogTitle" width="500">
          <span class = "text-enhancement-text">{{aiEnhancedText}}</span>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="dialogVisible = false">取消</el-button>
              <el-button type="primary" @click="insertText">
                插入
              </el-button>
            </div>
          </template>
        </el-dialog>
        <el-dialog
            class="knowledge-upload-dialog"
            v-model="knowledgeUploadDialogVisible"
            title="添加知识"
            width="700"
            :before-close="knowledgeUploadDialogHandleClose"
        >
          <el-upload
            class="knowledge-upload-dialog"
            drag
            action="/api/chat/upload/"
            multiple
            :limit="1"
            :on-exceed="handleExceed"
            :before-upload="beforeUpload"
            :file-list="fileList"
            :before-remove="knowledgeUploadHandleRemove"
            :on-success="handleSuccess"
          >
            <el-icon class="el-icon--upload"><upload-filled/></el-icon>
            <div class="el-upload__text">
              将文件拖至这里或者 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                仅支持pdf 单个文件不能超过20MB
              </div>
            </template>
          </el-upload>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="knowledgeUploadDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="handleUploadKnowledge">
                添加
              </el-button>
            </div>
          </template>
        </el-dialog>
        <el-drawer v-model="knowledgeRepositoryDrawer" title="管理知识库"  :before-close="knowledgeRepositoryDrawerHandleClose">
          <template #header>
            <h4>管理知识库</h4>
            <el-button class="knowledgeUploadPDFButton" type="primary" @click="showKnowledgeUploadDialog">新增</el-button>
          </template>
            <knowledge-repository-card
              v-for="(card, index) in knowledgeCards"
              :key="index"
              class="knowledge-repository-card"
              :title="card.source"
              :content="card.content"
              @documentDeleted="fetchKnowledgeCards"
            ></knowledge-repository-card>
        </el-drawer>
        <el-header class="header-menu">
          <div class="editor-menu" v-if="editor">
            <MenuBar :editor="editor" />
          </div>
        </el-header>
        <el-container>
          <bubble-menu
              :editor="editor"
              :tippy-options="{ duration: 100, placement: 'bottom' }"
              v-if="editor && bubbleMenuVisible"
            >
            <div class="bubble-menu-button">
              <el-button-group >
                <el-button @click="polishText">
                  润色
                </el-button>
                <el-button @click="summaryText">
                  摘要
                </el-button>
                <el-button @click="continueText">
                  续写
                </el-button>
                <el-button @click="correctText">
                  病句修改
                </el-button>
                <el-button @click="translateText">
                  翻译
                </el-button>
              </el-button-group>
            </div>
          </bubble-menu>
          <el-aside  class="left-aside sidebar">
            <TocPanel :items="toc" :editor="editor"/>
          </el-aside>
          <el-main class="editor-panel-main">
            <div class="editor-main" v-if="editor">
              <editor-content class="editor-content" :editor="editor"/>
              <div class="character-count" v-if="editor">
                {{ editor.storage.characterCount.characters() }} 字符
              </div>
            </div>
          </el-main>
          <el-aside class="aside right-aside">
            <chat-box></chat-box>
          </el-aside>
        </el-container>
      </el-container>
    </div>
  </el-container>
</template>

<script>

import {ArrowDown, ArrowLeft, ArrowRight, UploadFilled} from "@element-plus/icons-vue";
import {useEditor, EditorContent, VueNodeViewRenderer} from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import Highlight from '@tiptap/extension-highlight';
import TaskList from "@tiptap/extension-task-list";
import TaskItem from "@tiptap/extension-task-item";
import TextAlign from '@tiptap/extension-text-align'
import FontFamily from "@tiptap/extension-font-family";
import TextStyle from "@tiptap/extension-text-style";
import Underline from "@tiptap/extension-underline";
import CharacterCount from "@tiptap/extension-character-count";
import Mathematics from '@tiptap-pro/extension-mathematics';
import {getHierarchicalIndexes, TableOfContents} from "@tiptap-pro/extension-table-of-contents";
import FontSize from "tiptap-extension-font-size";
import Placeholder from '@tiptap/extension-placeholder';
import Image from '@tiptap/extension-image';
import Table from '@tiptap/extension-table';
import TableRow from '@tiptap/extension-table-row';
import TableCell from '@tiptap/extension-table-cell';
import TableHeader from '@tiptap/extension-table-header';
import Typography from '@tiptap/extension-typography';
import Color  from '@tiptap/extension-color';
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight';
import css from 'highlight.js/lib/languages/css';
import js from 'highlight.js/lib/languages/javascript';
import ts from 'highlight.js/lib/languages/typescript';
import html from 'highlight.js/lib/languages/xml';
import { lowlight } from 'lowlight/lib/core';
import Dropcursor from '@tiptap/extension-dropcursor'
import {BubbleMenu} from "@tiptap/vue-3";

lowlight.registerLanguage('html',html);
lowlight.registerLanguage('css',css);
lowlight.registerLanguage('js',js);
lowlight.registerLanguage('ts',ts);



import MenuBar from './MenuBar.vue';
import ChatBox from './Chat.vue'; // 确保路径正确
import CodeBlockComponent from './CodeBlockComponent.vue';
import TocPanel from "./TocPanel.vue";
import textEnhancements from '../../custom_extensions/textEnhancements.js'; // 引入自定义的扩展



import {onMounted, ref} from "vue";

import 'katex/dist/katex.min.css';
import '../../assets/EditorPanel.css';
import '../../assets/TiptapStyle.css';
import axios from "axios";
import KnowledgeRepositoryCard from "./KnowledgeRepositoryCard.vue";
import {ElMessage} from "element-plus";

import { defineProps, watch } from "vue";
import { useRoute } from "vue-router";
import router from "../../router/index.ts";

export default {
  name: 'EditorPanel',
  components: {
    UploadFilled,
    KnowledgeRepositoryCard,
    ArrowRight,
    ArrowDown,
    EditorContent,
    TocPanel,
    ChatBox,
    MenuBar,
    BubbleMenu,
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
    // 返回上一个页面
    const goBack = () =>{
      router.push("/space")
    }

    const titleText = ref("未命名")
    const saveTime = ref("文档已保存")
    const fileState = ref("允许编辑")
    const fileStateType = ref("primary")

    const initHtmlContent = ref("")
    const props = defineProps({
        id: {
          type: String,
          default: ()=>{
            return {}
         },
       },
    })
    const route = useRoute();
    const id = route.params.id;
    onMounted(async()=>{
      const response = await axios.get(`/api/user/document/get/${id}/`)
      const data = response.data;
      initHtmlContent.value = data[0].content;
      editor.value.commands.insertContent(initHtmlContent.value)
      titleText.value = data[0].name;
    })

    //文档保存函数
    const saveDocument = async () => {
      const htmlContent = editor.value.getHTML();
      // 正则表达式匹配 id 和 data-toc-id 属性及其值
      const regex = /\s*(id|data-toc-id)="[^"]*"/g;
      // 使用正则表达式替换匹配的部分为空字符串，即删除匹配的部分
      const cleanedText = htmlContent.replace(regex, '');
      saveTime.value =' 文档已保存 ' + new Date().toLocaleString();
      console.log(cleanedText)
      // 更新文档标题
      const $doc = editor.value.$doc;
      const firstH1 = $doc.querySelector("heading", { level: 1 });
      if (firstH1) {
        titleText.value = firstH1.textContent;
      } else {
        titleText.value = "未命名"
        // 如果没有H1
        console.warn('No <h1> found in the document.');
      }

      try {
        await axios.patch(`/api/user/document/update/${id}/`, {
          content: cleanedText,
          name: titleText.value
        });
        saveTime.value =' 文档已保存 ' + new Date().toLocaleString();
        // 更新文档标题
        const $doc = editor.value.$doc;
        const firstH1 = $doc.querySelector("heading", { level: 1 });
        if (firstH1) {
          titleText.value = firstH1.textContent;
        } else {
          titleText.value = "未命名"
          // 如果没有H1
          console.warn('No <h1> found in the document.');
        }
        await axios.patch(`/api/user/files/updatefile/${id}/`, {
          name: titleText.value
        });
      } catch (error) {
           console.error('保存文档失败', error);
      }
    };
    // 自动调用计时器保存
    setInterval(saveDocument, 60000); // 每分钟调用一次 saveDocument

    //保存为模板函数
    const saveFormat = async () => {
      await saveDocument(); // 保存为模板前先调用一次保存文档函数
      const htmlContent = editor.value.getHTML();
      // 正则表达式匹配 id 和 data-toc-id 属性及其值
      const regex = /\s*(id|data-toc-id)="[^"]*"/g;
      // 使用正则表达式替换匹配的部分为空字符串，即删除匹配的部分
      const cleanedText = htmlContent.replace(regex, '');
      const userName = localStorage.getItem("username")
      const $doc = editor.value.$doc;
      const firstH1 = $doc.querySelector("heading", { level: 1 });
      if (firstH1) {
        titleText.value = firstH1.textContent;
      } else {
        titleText.value = "未命名"
        // 如果没有H1
        console.warn('No <h1> found in the document.');
      }

      try {
        await axios.post(`/api/user/template/`, {
          name: titleText.value,
          content: cleanedText,
          image_path: "https://as.smgv.cn/static/template/icons/new/doc.png",
          username: userName
        });
      } catch (error) {
        console.error('保存模板失败', error);
      }
    };

    //修改文档编辑状态函数
    const changeFileStateFalse = () => {
      editor.value.setEditable(false);
      fileState.value = '只读';
      fileStateType.value = 'warning';
    };
    const changeFileStateTrue = () => {
      {
        editor.value.setEditable(true);
        fileState.value = '允许编辑';
        fileStateType.value = 'primary';
      }
    };

    const knowledgeRepositoryDrawer = ref(false) //知识库管理抽屉显示状态
    const knowledgeUploadDialogVisible = ref(false)

    const fileList = ref([]);  // 文件列表
    const handleSuccess = (response, file, uploadFileList) => {
      fileList.value = uploadFileList;
      ElMessage.success('文件上传成功');
    };

    //文件上传函数
    const beforeUpload = (file) => {
      const fileType = file.type;
      const validExtensions = ['application/pdf'];
      const isAllowedExtension = validExtensions.includes(fileType);

      if (!isAllowedExtension) {
        ElMessage.error('支持的文件格式：pdf');
        return false;
      }

      const isLt20MB = file.size / (1024 * 1024) < 20; // Check if file size is less than 20MB
      if (!isLt20MB) {
        ElMessage.error('文件大小不能超过20MB');
        return false;
      }

      return true;
    }

    const knowledgeCards = ref([]);
    // 获得知识卡片列表
    const fetchKnowledgeCards = async () => {
      try {
        const userId = localStorage.getItem("user_id");
        const response = await axios.get(`/api/dialogue/getKB/${userId}/`);

        // 清空之前的卡片数据
        knowledgeCards.value = [];

        // 遍历响应中的每个条目并创建对应的卡片对象
        response.data.知识库的内容.forEach((item) => {
          const card = {
            content: item.content,
            source: item.source
          };
          console.log(card)
          knowledgeCards.value.push(card);
        });

      } catch (error) {
        console.error("Failed to fetch knowledgeCards data:", error);
      }
    };

    const handleExceed = (files) => {
      ElMessage.error('最多上传一个文件！');
    };
    const openKnowledgeRepositoryDrawer = () => {
      fetchKnowledgeCards();
      knowledgeRepositoryDrawer.value = true;
    }
    const knowledgeRepositoryDrawerHandleClose = () => {
        knowledgeRepositoryDrawer.value = false;
    }
    const showKnowledgeUploadDialog = () =>{
      fileList.value = []; // 清空上传的文件列表
      knowledgeUploadDialogVisible.value = true;
    }


    // 确定添加上传的pdf
    const handleUploadKnowledge = () =>{
      // 获取上传成功的文件
      if (fileList.value.length === 0) {
        ElMessage.error("请先上传一个文件");
        return;
      }

      const file = fileList.value[0]; // 假设只上传一个文件
      const formData = new FormData();
      formData.append("file", file.raw); // 使用上传的文件

      const userId = localStorage.getItem("user_id");
      // 发送PDF到后端录入知识库
      axios
        .post(`/api/dialogue/addNewPDF/${userId}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          fetchKnowledgeCards()
          ElMessage.success("新知识添加成功！")
        })
        .catch((error) => {
          ElMessage.error("新知识添加失败！");
        });
    }

    // 删除上传的文件
    const knowledgeUploadDialogHandleClose = () =>{
      if (fileList.value.length === 0) {
        knowledgeUploadDialogVisible.value = false; // 销毁对话框
        return;
      }
      const file = fileList.value[0]; // 假设只上传一个文件
      const formData = new FormData();

      formData.append("file", file.raw); // 使用上传的文件
      axios
        .post("/api/chat/delatemultifile/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
          .then(() => {
            knowledgeUploadDialogVisible.value = false; // 销毁对话框
        })
          .catch((error) => {
            knowledgeUploadDialogVisible.value = false; // 销毁对话框
          });
    }

    //
    const knowledgeUploadHandleRemove = (file) =>{
      const formData = new FormData();

      formData.append("file", file.raw); // 使用上传的文件
      axios
        .post("/api/chat/delatemultifile/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
          .then(() => {

        })
          .catch((error) => {

          });
    }

    const toc = ref([])
    const editor = useEditor({
     content: initHtmlContent.value,
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
          types: ['heading', 'paragraph', 'image'],
        }),
        FontFamily.configure({
          types: ['textStyle'],
        }),
        Underline.configure({
        }),
        CharacterCount.configure({
            mode: 'textSize',
        }),
        Mathematics,
        TableOfContents.configure({
          getIndex: getHierarchicalIndexes,
          onUpdate(content) {
            toc.value = content.map(item => (
                {
              id: item.id,
              text: item.textContent,
              level: item.level,
              isActive: item.isActive,
              isScrolledOver: item.isScrolledOver,
            }));
          },
        }),
        Placeholder.configure({
          placeholder: '写点什么吧...',
        }),
        StarterKit,
        Image.configure({
          inline: true,
        }),
        Typography,
        CodeBlockLowlight.extend({
            addNodeView() {
              return VueNodeViewRenderer(CodeBlockComponent)
            },
        }).configure({ lowlight }),
        Color,
        textEnhancements,
        Dropcursor,
      ]
    })

    const aiEnhancedText = ref('');  // 存储ai增强后的文本
    const dialogVisible = ref(false);  // 设置对话框是否可见
    const dialogTitle = ref('');  // 设置对话框标题
    const loading = ref(false);  // 设置加载状态
    const bubbleMenuVisible = ref(true);   // 设置bubble_menu是否可见

    // ai总结
    const summaryText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      await editor.value.chain().focus().summaryText((text) => {
        dialogTitle.value = '摘要结果'; // 修改对话框标题
        aiEnhancedText.value = text.response;  // 修改对话框面板内容
        loading.value = false;
        bubbleMenuVisible.value = true;
        dialogVisible.value = true; // 显示对话框
      }).run();
    };

    // ai润色
    const polishText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      await editor.value.chain().focus().polishText((text) => {
        dialogTitle.value = '润色结果'; // 修改对话框标题
        aiEnhancedText.value = text.response;  // 修改对话框面板内容
        loading.value = false;
        bubbleMenuVisible.value = true;
        dialogVisible.value = true; // 显示对话框
      }).run();
    };

    // ai续写
    const continueText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      await editor.value.chain().focus().continuationText((text) => {
        dialogTitle.value = '续写结果'; // 修改对话框标题
        aiEnhancedText.value = text.response;  // 修改对话框面板内容
        loading.value = false;
        bubbleMenuVisible.value = true;
        dialogVisible.value = true; // 显示对话框
      }).run();
    };

    // ai纠错
    const correctText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      await editor.value.chain().focus().correctText((text) => {
        dialogTitle.value = '纠错结果'; // 修改对话框标题
        aiEnhancedText.value = text.response;  // 修改对话框面板内容
        loading.value = false;
        bubbleMenuVisible.value = true;
        dialogVisible.value = true; // 显示对话框
      }).run();
    };

    // ai翻译
    const translateText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      await editor.value.chain().focus().translateText((text) => {
        dialogTitle.value = '翻译结果'; // 修改对话框标题
        aiEnhancedText.value = text.response;  // 修改对话框面板内容
        loading.value = false;
        bubbleMenuVisible.value = true;
        dialogVisible.value = true; // 显示对话框
      }).run();
    };

    // ai插入
    const insertText = () => {
      const { from, to } = editor.value.state.selection;
      const position = { from, to };  // 构建位置对象
      editor.value.commands.insertContentAt(position, aiEnhancedText.value)
      aiEnhancedText.value = ''; // 清除面板内容
      dialogTitle.value =''; // 清楚对话框标题内容
      dialogVisible.value = false; // 关闭对话框
    };

    const leftAsideVisable = ref(false)

    return {
      goBack,
      titleText,
      saveTime,
      fileState,
      fileStateType,
      initHtmlContent,
      knowledgeRepositoryDrawer,
      knowledgeUploadDialogVisible,
      fileList,
      saveDocument,
      saveFormat,
      changeFileStateTrue,
      changeFileStateFalse,
      handleSuccess,
      beforeUpload,
      handleExceed,
      openKnowledgeRepositoryDrawer,
      showKnowledgeUploadDialog,
      handleUploadKnowledge,
      knowledgeUploadDialogHandleClose,
      knowledgeUploadHandleRemove,
      knowledgeRepositoryDrawerHandleClose,
      knowledgeCards,
      fetchKnowledgeCards,
      editor,
      toc,
      dialogVisible,
      dialogTitle,
      aiEnhancedText,
      polishText,
      summaryText,
      continueText,
      correctText,
      translateText,
      insertText,
      loading,
      bubbleMenuVisible,
      leftAsideVisable
    }
  }
}


</script>


<style scoped lang="scss">

.header-dropdown-menu-file {
  cursor: pointer;
}
.knowledge-repository-card{
  width: 100%;
  height: 20rem;
  margin-top: 10px;
}
.title-text {
  font-weight: bold;
}
.save-time{
  color: lightgray;
}
.header-dropdown-menu-file{
  height: 1.25rem;
}
.body{
  height: 95vh;
  width: 98vw;
}
</style>