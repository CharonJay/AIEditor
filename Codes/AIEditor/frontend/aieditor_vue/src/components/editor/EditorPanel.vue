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
            <el-dropdown-menu >
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
          <el-button v-if="status == 1" link class="collaborate-button" type="primary" @click="shareDocument">
            邀请他人一起协作
          </el-button>
        <el-text class="file-state" :type="fileStateType">{{fileState}}</el-text>
        <el-text class="save-time">{{saveTime}}</el-text>
      </el-space>
    </template>
  </el-page-header>
  <el-container class="body">
    <div class="common-layout">
      <el-container v-loading.fullscreen.lock="loading" element-loading-text="AI正在努力中..." class="parent-container">
        <el-dialog class = "share-document-dialog" v-model="shareDocumentDialogVisible" title = "分享文档" width = "500">
          <p>将这段分享码分享给其他人吧！</p>
          <p>{{ inviteCode }}</p>
        </el-dialog>
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
        <div>
          <el-dialog @before-close="bubbleMenuVisible=true" class="str2imgDialogMenu" v-model="dialogFormVisible" title="智能绘图" width="500">
            <el-form :model="form">
              <!-- Form fields -->
              <el-form-item label="图片名称" :label-width="formLabelWidth">
                <el-input v-model="form.imageName" placeholder="图片名称" />
              </el-form-item>
              <el-form-item label="风格" :label-width="formLabelWidth">
                <el-select v-model="form.style" placeholder="请输入风格" filterable allow-create>
                  <el-option v-for="item in styleOptions" :key="item" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="主体" :label-width="formLabelWidth">
                <el-select v-model="form.subject" placeholder="请输入主体" filterable allow-create>
                  <el-option v-for="item in subjectOptions" :key="item" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="描述" :label-width="formLabelWidth">
                <el-select v-model="form.description" placeholder="请输入描述" filterable allow-create multiple>
                  <el-option v-for="item in descriptionOptions" :key="item" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="效果" :label-width="formLabelWidth">
                <el-select v-model="form.effect" placeholder="请输入效果" filterable allow-create>
                  <el-option v-for="item in effectOptions" :key="item" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="文本内容" :label-width="formLabelWidth">
                <el-input v-model="form.otherContent"  type="textarea" placeholder="请输入其他内容" :rows="10"/>
              </el-form-item>
            </el-form>
            <template #footer>
              <div class="dialog-footer">
                <el-button @click="dialogFormVisible = false; bubbleMenuVisible=true">取消</el-button>
                <el-button type="primary" @click="handleSubmit">确定</el-button>
              </div>
            </template>
          </el-dialog>
          <el-dialog @before-close="bubbleMenuVisible=true" class="str2imgDialogImg" v-model="dialogImageVisible" title="生成图片" width="600">
            <div v-if="imageUrl">
              <img :src="imageUrl" alt="生成的图片" style="width: 100%;" />
            </div>
            <div v-else>
              <p>正在绘制，请稍等...</p>
            </div>
            <template #footer>
              <div class="dialog-footer">
                <el-button v-if="imageUrl" @click="insertImage">插入</el-button>
              </div>
            </template>
          </el-dialog>
    </div>
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
        <div class="knowledgeRepositoryDrawer">
          <el-drawer v-model="knowledgeRepositoryDrawerVisible" title="管理知识库" :before-close="knowledgeRepositoryDrawerHandleClose">
            <template #header>
              <h4>管理知识库</h4>
              <el-button class="knowledgeUploadPDFButton" type="primary" @click="showKnowledgeUploadDialog">新增</el-button>
            </template>
            <el-space wrap :size="30">
              <knowledge-repository-card
                v-for="(card, index) in knowledgeCards"
                :key="index"
                class="knowledge-repository-card"
                :title="card.source"
                :content="card.content"
                @documentDeleted="fetchKnowledgeCards"
              ></knowledge-repository-card>
            </el-space>
          </el-drawer>
        </div>
        <el-header class="header-menu">
          <div class="editor-menu" v-if="editor">
            <MenuBar :editor="editor"  :title-text="titleText"/>
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
                <el-button @click="polishText" text bg>
                  <i class="ri-bard-line"></i>
                  润色
                </el-button>
                <el-button @click="summaryText" text bg>
                  <i class="ri-file-list-3-line"></i>
                  摘要
                </el-button>
                <el-button @click="continueText" text bg>
                  <i class="ri-edit-2-line"></i>
                  续写
                </el-button>
                <el-button @click="correctText" text bg>
                  <i class="ri-first-aid-kit-line"></i>
                  病句修改
                </el-button>
                <el-button @click="translateText"  text bg>
                  <i class="ri-translate"></i>
                  翻译
                </el-button>
                <el-button @click=" text2Img"  text bg>
                  <i class="ri-translate"></i>
                  文生图
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
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import {ArrowDown, ArrowLeft, ArrowRight, UploadFilled} from "@element-plus/icons-vue";
import {useEditor, Editor, EditorContent, VueNodeViewRenderer} from '@tiptap/vue-3';
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



import MenuBar from '@/components/editor/MenuBar.vue';
import ChatBox from '@/components/editor/Chat.vue';
import CodeBlockComponent from '@/components/editor/CodeBlockComponent.vue';
import TocPanel from "@/components/editor/TocPanel.vue";
import MindMapPanel from "@/components/editor/MindMapPanel.vue";
import KnowledgeRepositoryCard from "@/components/editor/KnowledgeRepositoryCard.vue";

import textEnhancements from '@/custom_extensions/textEnhancements.js'; // 引入自定义的扩展

import {reactive, onMounted, ref} from "vue";
import {ElLoading, ElMessage, ElMessageBox} from "element-plus";
import axios from "axios";
import { defineProps} from "vue";
import { useRoute } from "vue-router";

import 'katex/dist/katex.min.css';
import '@/assets/EditorPanel.css';
import '@/assets/TiptapStyle.css';
import '@/assets/remixicon/remixicon.css'

import router from "@/router/index.ts";

import Collaboration from '@tiptap/extension-collaboration'
import * as Y from 'yjs'
import { TiptapCollabProvider } from '@hocuspocus/provider'
import { onUnmounted } from "vue";
import CollaborationCursor from '@tiptap/extension-collaboration-cursor'



export default {
  name: 'EditorPanel',
  components: {
    UploadFilled,
    KnowledgeRepositoryCard,
    ArrowRight,
    ArrowDown,
    EditorContent,
    TocPanel,
    MindMapPanel,
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
    const route = useRoute();
    const id = route.params.id;
    const status = route.params.status

    // 返回上一个页面
    const goBack = () =>{
      router.push("/space")
    }
    // ------协作-----
    const doc = new Y.Doc() // Initialize Y.Doc for shared editing

    const titleText = ref("未命名")
    const saveTime = ref("文档已保存")
    const fileState = ref("允许编辑")
    const fileStateType = ref("primary")
    const mycolor = '#' + Math.floor(Math.random() * 16777215).toString(16)
    const inviteCode = btoa(`document${id}`, 'e97e0vk0')
    const shareDocumentDialogVisible = ref(false)

    const shareDocument = () => {
      shareDocumentDialogVisible.value = true;
    }

    const initHtmlContent = ref("")
    const props = defineProps({
        id: {
          type: String,
          default: ()=>{
            return {}
         },
       },
    })

    const provider = new TiptapCollabProvider({
        name: `document${id}`,
        appId: 'e97e0vk0',
        token: localStorage.getItem('access_token'),
        document: doc,
        forceSyncInterval: 1000,
        onOpen() {
          console.log('WebSocket connection opened.')
        },
        onConnect() {
          console.log('Connected to Collab server')
        },
        onAuthenticated() {
          console.log('Authenticated')
        },
        onAuthenticationFailed({reason}){
          console.log('Authentication failed')
          console.error('Authentication failed:', reason)
        },
        onStatus(){
          console.log('Status changed')
        },
        onSynced() {
          if (!doc.getMap('config').get('initialContentLoaded') && editor) {
            doc.getMap('config').set('initialContentLoaded', true)
          }
          console.log('Synced')
        },
      })



    onMounted(async()=>{
      const response = await axios.get(`/api/user/document/get/${id}/`)
      const data = response.data;
      initHtmlContent.value = data[0].content;
      titleText.value = data[0].name;
    })
    // ------协作者设置-----
    provider.on('synced', () => {
      console.log('Document synced.')
    })
    provider.setAwarenessField('user', {
      // Share any information you like
      name: localStorage.getItem('username'),
      color: mycolor,
    })

    document.addEventListener('mousemove', (event) => {
      // Share any information you like
      provider.setAwarenessField('user', {
        name: localStorage.getItem('username'),
        color: mycolor,
        mouseX: event.clientX,
        mouseY: event.clientY,
      })
    })


    //文档保存函数
    const saveDocument = async () => {
      const htmlContent = editor.value.getHTML();
      // 正则表达式匹配 id 和 data-toc-id 属性及其值
      const regex = /\s*(id|data-toc-id)="[^"]*"/g;
      // 使用正则表达式替换匹配的部分为空字符串，即删除匹配的部分
      const cleanedText = htmlContent.replace(regex, '');
      initHtmlContent.value = cleanedText;
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
      // 保存内容中的标题
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

    const knowledgeRepositoryDrawerVisible = ref(false) //知识库管理抽屉显示状态
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
      knowledgeRepositoryDrawerVisible.value = true;
    }
    const knowledgeRepositoryDrawerHandleClose = () => {
        knowledgeRepositoryDrawerVisible.value = false;
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

      // 显示加载状态
      const loadingInstance = ElLoading.service({
        lock: true,
        text: '知识添加中...',
      });

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
        })
        .finally(() => {
          // 隐藏加载状态
          loadingInstance.close();
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
        Document,
        Text,
        // ---------协作设置----------
        Collaboration.configure({
          document: doc,
        }),
        CollaborationCursor.configure({
          provider: provider,
          user: {
            name: localStorage.getItem('username'),
            color: mycolor,
          },
        }),

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
        StarterKit.configure({
          codeBlock: false, // 排除codeBlock避免重复引用
          dropcursor:false, // 排除dropcursor避免重复引用
        }),
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
    const position = ref({});

    // ai润色
    const polishText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      const { from, to } = editor.value.state.selection;
      position.value = { from, to };  // 构建位置对象
      await editor.value.chain().focus().polishText((text) => {
        dialogTitle.value = '润色结果'; // 修改对话框标题
        aiEnhancedText.value = text.response;  // 修改对话框面板内容
        loading.value = false;
        bubbleMenuVisible.value = true;
        dialogVisible.value = true; // 显示对话框
      }).run();
    };

    // ai总结
    const summaryText = async () => {
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      dialogTitle.value = '';
      aiEnhancedText.value = ''; // 清除面板内容
      loading.value = true;
      const { from, to } = editor.value.state.selection;
      position.value = { from, to };  // 构建位置对象
      await editor.value.chain().focus().summaryText((text) => {
        dialogTitle.value = '摘要结果'; // 修改对话框标题
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
      const { from, to } = editor.value.state.selection;
      position.value = { from, to };  // 构建位置对象
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
      const { from, to } = editor.value.state.selection;
      position.value = { from, to };  // 构建位置对象
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
      const { from, to } = editor.value.state.selection;
      position.value = { from, to };  // 构建位置对象
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
      editor.value.commands.insertContentAt(position.value, aiEnhancedText.value)
      aiEnhancedText.value = ''; // 清除面板内容
      dialogTitle.value =''; // 清楚对话框标题内容
      dialogVisible.value = false; // 关闭对话框
    };


    const leftAsideVisable = ref(false)

    const form = reactive({
      style: '',
      subject: '',
      description: [],
      effect: '',
      imageName: '',
      otherContent: '',
    })
  
    const styleOptions = [
      '古风', '二次元', '写实风格', '浮世绘', '未来主义', '像素风格', '概念艺术', '赛博朋克', '洛丽塔风格',
      '巴洛克风格', '超现实主义', '水彩画', '蒸汽波艺术', '油画', '卡通画', '梵高', '罗伊里奇', '莫奈',
      '毕加索', '毕沙罗', '多雷', '齐白石', '艺术创想', '唯美二次元', '怀旧漫画风', '中国风', '概念插画',
      '明亮插画', '梵高', '超现实主义', '动漫风', '插画', '像素艺术', '炫彩插画'
    ]
  
    const subjectOptions = [
      '老人', '童话世界', '兔子', '老照片', '超级英雄', '竹林', '日出', '少女'
    ]
  
    const descriptionOptions = [
      '星辰大海', '盛世牡丹', '晶莹剔透', '喜闻乐见', '星月神话', '满庭芬芳', '精致面容', '对称美学', '唯美',
      '看镜头', '精致美丽的五官', '华丽装饰', '绝美头饰', '浪漫色调', '几何构成', '丰富细节', '虚幻引擎'
    ]
  
    const effectOptions = [
      '高清8k壁纸', '极致细节', '精细刻画', '超高清', '优化效果', '令人惊叹的3D渲染', '灵感艺术', '完美光影精美的CG',
      '剧照', '色彩丰富', '建筑素描', '3D风格', '真实感', '超写实风', '高对比度', '马卡龙质感', '完美彩色炫酷涂装',
      '流线型外观设计', '低纯度色调', '高纯度色调', '多色彩搭配', '光影追踪', '宫崎骏风格', '电影瞬间', '层次感'
    ]
    const dialogFormVisible = ref(false)
    const dialogImageVisible = ref(false)
    const imageUrl = ref('')
    const formLabelWidth = '140px'

    // 文生图
    const text2Img = () => {
      dialogFormVisible.value = true;
      bubbleMenuVisible.value = false; // 隐藏bubble_menu
      const { from, to } = editor.value.state.selection;
      position.value = { from, to };  // 构建位置对象
      form.otherContent = editor.value.state.doc.textBetween(from, to, ' ');  // 将选中的文本内容赋值给 otherContent
    };
    const handleSubmit = async () => {
      if (!form.subject) {
        ElMessageBox.alert('请填写主体内容', '提示', {
          confirmButtonText: '确定',
          type: 'warning',
        })
        return
      }

      if (!form.imageName) {
        form.imageName = 'picture'
      }

      try {
        dialogImageVisible.value = true  // 显示正在绘制的对话框
        imageUrl.value = ''  // 清空之前的图片 URL
        const response = await axios.post('/api/chat/generate-image/', form)
        if (response.data.img_url) {
          imageUrl.value = response.data.img_url
          console.log('表单提交成功:', response.data)
        } else {
          console.error('图片生成失败:', response.data)
        }
      } catch (error) {
        console.error('表单提交失败:', error)
      }
    }
  
    const insertImage = () => {
      // 插入图片的逻辑，例如将图片 URL 插入到富文本编辑器
      console.log('插入图片:', imageUrl.value)
      bubbleMenuVisible.value = true
      dialogImageVisible.value = false
      dialogFormVisible.value = false
      const imgText = `<img src="${imageUrl.value}"/>`;
      editor.value.commands.insertContentAt(position.value, imgText)
    }

    return {
      goBack,
      titleText,
      saveTime,
      fileState,
      fileStateType,
      initHtmlContent,
      knowledgeRepositoryDrawerVisible,
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
      text2Img,
      loading,
      bubbleMenuVisible,
      leftAsideVisable,
      styleOptions,
      subjectOptions,
      descriptionOptions,
      effectOptions,
      handleSubmit,
      dialogImageVisible,
      dialogFormVisible,
      formLabelWidth,
      insertImage,
      form,
      imageUrl,
      position,

       // 协作
      shareDocument,
      inviteCode,
      shareDocumentDialogVisible,
      status
    }
  }
}


</script>


<style scoped lang="scss">
/* Give a remote user a caret */
:deep(.collaboration-cursor__caret) {
    border-left: 1px solid #0d0d0d;
    border-right: 1px solid #0d0d0d;
    margin-left: -1px;
    margin-right: -1px;
    pointer-events: none;
    position: relative;
    word-break: normal;
  }

  /* Render the username above the caret */
:deep(.collaboration-cursor__label) {
    border-radius: 3px 3px 3px 0;
    color: #0d0d0d;
    font-size: 12px;
    font-style: normal;
    font-weight: 600;
    left: -1px;
    line-height: normal;
    padding: 0.1rem 0.3rem;
    position: absolute;
    top: -1.4em;
    user-select: none;
    white-space: nowrap;
  }
.collaborate-button{
  justify-items: center;
  align-items: center;
}

.bubble-menu-button {
  width: 30vw;
}
.header-dropdown-menu-file {
  align-items: center;
  cursor: pointer;
}
.knowledgeRepositoryDrawer:deep(.el-drawer__header) {
  margin-bottom: 0;
  padding: 10px;
}

.knowledge-repository-card{
  width: 100%;
  height: 20rem;
}
.title-text {
  font-weight: bold;
}
.save-time{
  color: lightgray;
}
.body{
  height: 95vh;
  width: 98vw;
}

</style>