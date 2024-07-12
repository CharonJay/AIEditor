<template>
  <el-dialog :before-close="handleClose" class="ai-multi-model-process-dialog" v-model="multiModelDialogVisible" title="智能识别" width="1300" >
    <div v-loading="loading" element-loading-text="拼命加载中...">
      <el-row>
        <el-col class="ai-multi-model-process-dialog-col" :span="11">
          <h3>上传文件</h3>
          <el-upload
            class="ai-multi-model-process-dialog-upload"
            drag
            action="/api/chat/upload/"
            multiple
            :limit="1"
            :on-exceed="handleExceed"
            :before-upload="beforeUpload"
            :on-remove="handleRemove"
            :file-list="fileList"
            :on-success="handleSuccess"
          >
            <el-icon class="el-icon--upload"><upload-filled/></el-icon>
            <div class="el-upload__text">
              将文件拖至这里或者 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持格式：png、jpg、jpeg、pdf、pdf、mpeg、wav、ogg、flac 单个文件不能超过20MB
              </div>
            </template>
          </el-upload>
        </el-col>
        <el-col class="ai-multi-model-process-dialog-col" :span="11" :offset="2">
          <h3>智能识别结果</h3>
          <el-card class="ai-multi-model-process-dialog-card" shadow="never">
            <el-empty class="ai-multi-model-process-dialog-empty" v-if="multiModelEmptyVisible" description="试试上传文件吧"   :image-size="80"/>
              <div class="scrollable-content" v-if="recognitionResult !== ''">{{recognitionResult}}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-row>
        <el-col class="ai-multi-model-process-dialog-col" :span="3" :offset="18">
          <el-button class="ai-multi-model-process-dialog-button" @click="startOCR" type="primary">识别转录</el-button>
        </el-col>
        <el-col class="ai-multi-model-process-dialog-col" :span="2" :offset="0">
          <el-button class="ai-multi-model-process-dialog-button" @click="insertKnowledgeRepository" type="primary">录入知识库</el-button>
        </el-col>
      </el-row>
    </div>

  </el-dialog>
  <div>
    <formatting-template-dialog
        v-model="formattingTemplateDiaLogVisible"
        :formatting-template-dia-log-visible="formattingTemplateDiaLogVisible"
        @useFormatEvent="formatDocument"
    />
  </div>
  <div>
    <template v-for="(item, index) in items" :key="index">
      <el-divider class="menu-item-divider" v-if="item.type === 'divider'" :key="`divider${index}`" direction="vertical" />
      <menu-button-dropdown-item v-else-if="item.type === 'buttonDropdown'" :key="`buttonDropdown${index}` " v-bind="item"/>
      <menu-option-item v-else-if="item.type === 'selector'" :key="`selector${index}`" v-model="selectedValues[index]" v-bind="item"/>
      <menu-color-item v-else-if="item.type === 'colorPicker'" :key="`colorPicker${index}`" :title="item.title" :initialColor="item.color" :onChange="(color) => updateColor(index, color)" />
      <menu-button-item v-else :key="index" v-bind="item" />
    </template>
  </div>
</template>

<script>
import MenuButtonItem from './MenuButtonItem.vue';
import MenuOptionItem from "./MenuOptionItem.vue";
import MenuButtonDropdownItem from "./MenuButtonDropdownItem.vue";
import MenuColorItem from "./MenuColorItem.vue";
import {reactive, ref} from "vue";
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { UploadFilled } from '@element-plus/icons-vue'
import {ElLoading, ElMessage} from 'element-plus';
import axios from 'axios'
import FormattingTemplateDialog from "./FormattingTemplateDialog.vue";
import {useRoute} from "vue-router";
export default {
  components: {
    FormattingTemplateDialog,
    UploadFilled,
    MenuButtonItem,
    MenuOptionItem,
    MenuButtonDropdownItem,
    MenuColorItem
  },

  props: {
    editor: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    // 控制对话框显示状态的变量
    const multiModelDialogVisible = ref(false);
    const multiModelEmptyVisible = ref(false)

    const fileList = ref([]);
    const handleSuccess = (response, file, uploadFileList) => {
      fileList.value = uploadFileList;
      ElMessage.success('文件上传成功');
    };

    const beforeUpload = (file) => {
      const fileType = file.type;
      const validExtensions = ['image/png', 'image/jpg', 'image/jpeg', 'application/pdf', 'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/flac'];
      const isAllowedExtension = validExtensions.includes(fileType);

      if (!isAllowedExtension) {
        ElMessage.error('支持的文件格式：png、jpg、jpeg、pdf、mpeg、wav、ogg、flac');
        return false;
      }

      const isLt20MB = file.size / (1024 * 1024) < 20; // Check if file size is less than 20MB
      if (!isLt20MB) {
        ElMessage.error('文件大小不能超过20MB');
        return false;
      }

      return true;
    }
    const handleExceed = (files) => {
      ElMessage.error('最多上传一个文件！');
    };

    const items = reactive([
      {
        icon: 'arrow-go-back-line',
        title: '撤回',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().undo().run();
          }
          else {
            ElMessage.warning("当前文档为只读状态，禁止编辑")
          }
        }
      },
      {
        icon: 'arrow-go-forward-line',
        title: '前进',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().redo().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'format-clear',
        title: '清除所有格式',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().clearNodes().unsetAllMarks().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'text-wrap',
        title: '强制换行',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setHardBreak().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'divider'
      },
      {
        icon: 'bold',
        title: '加粗',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleBold().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'underline',
        title: '下划线',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleUnderline().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'italic',
        title: '斜体',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleItalic().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'font-color',
        title: '字体颜色',
        type: 'colorPicker',
        action: (color) => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setColor(color).run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'strikethrough',
        title: '中划线',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleStrike().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'mark-pen-line',
        title: '高亮',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleHighlight().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'divider'
      },
      {
        icon: 'align-left',
        title: '左对齐',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setTextAlign('left').run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'align-center',
        title: '居中对齐',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setTextAlign('center').run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'align-right',
        title: '右对齐',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setTextAlign('right').run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'align-justify',
        title: '两端对齐',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setTextAlign('justify').run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'divider'
      },
      {
        icon: 'paragraph',
        title: '段落',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setParagraph().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'buttonDropdown',
        icon: 'heading',
        title: '标题',
        options: [
          {
            label: '一级标题',
            value: '1',
          },
          {
            label: '二级标题',
            value: '2',
          },
          {
            label: '三级标题',
            value: '3',
          },
          {
            label: '四级标题',
            value: '4',
          },
          {
            label: '五级标题',
            value: '5',
          },
          {
            label: '六级标题',
            value: '6',
          }
        ],
        action: (value) => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleHeading({ level: parseInt(value) }).run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        },
      },
      {
        type: 'buttonDropdown',
        icon: 'font-family',
        title: '字体',
        options: [
          {
            label: '宋体',
            value: 'SimSun',
          },
          {
            label: '黑体',
            value: 'SimHei',
          },
          {
            label: '微软雅黑',
            value: 'Microsoft Yahei',
          },
          {
            label: '微软正黑体',
            value: 'Microsoft JhengHei',
          },
          {
            label: '楷体',
            value: 'KaiTi',
          },
          {
            label: '新宋体',
            value: 'NSimSun',
          },
          {
            label: '仿宋',
            value: 'FangSong',
          },
          {
            label: '华文细黑',
            value: 'STXihei',
          },
          {
            label: 'Arial',
            value: 'Arial',
          },
          {
            label: 'Times New Roman',
            value: 'Times New Roman',
          },
          {
            label: 'Monospace',
            value: 'monospace',
          },
        ],
        action: (value) => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setFontFamily(value).run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'buttonDropdown',
        icon: 'font-size',
        title: '字号',
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
        action: (value) => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setFontSize(value).run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'divider'
      },
      {
        icon: 'list-unordered',
        title: '无序列表',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleBulletList().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'list-ordered',
        title: '有序列表',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleOrderedList().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'list-check-2',
        title: '任务列表',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleTaskList().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'code-box-line',
        title: '代码块',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleCodeBlock().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'double-quotes-l',
        title: '引用',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().toggleBlockquote().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'separator',
        title: '水平分割线',
        action: () => {
          if (props.editor.isEditable) {
            props.editor.chain().focus().setHorizontalRule().run();
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        type: 'divider'
      },

      {
        icon: 'image-line',
        title: '插入图片',
        action: () => {
          if (props.editor.isEditable) {
            const url = window.prompt('请输入图片 URL');
            if (url) {
              props.editor.chain().focus().setImage({ src: url }).run();
            }
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'file-pdf-2-fill',
        title: '导出为PDF',
        action: async () => {
          const htmlContent = props.editor.getHTML();
          console.log(htmlContent);

          // 创建一个隐藏的 div 来渲染 HTML
          const tempDiv = document.createElement('div');
          tempDiv.style.position = 'absolute';
          tempDiv.style.top = '-9999px';
          tempDiv.innerHTML = htmlContent;
          document.body.appendChild(tempDiv);

          // 使用 html2canvas 将 HTML 转换为 Canvas
          const canvas = await html2canvas(tempDiv, { scale: 2 });

          // 创建 PDF 并将 Canvas 添加到 PDF 中
          const pdf = new jsPDF('p', 'mm', 'a4');
          const pdfWidth = pdf.internal.pageSize.getWidth();
          const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
          pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, pdfWidth, pdfHeight);

          // 下载 PDF
          pdf.save('document.pdf');

          // 移除临时 div
          document.body.removeChild(tempDiv);
        }
      },
      {
        icon: 'layout-horizontal-line',
        title: '智能排版',
        action: () => {
          if (props.editor.isEditable) {
            formattingTemplateDiaLogVisible.value = true;
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
      {
        icon: 'file-upload-line',
        title: '智能识别',
        action: () => {
          if (props.editor.isEditable) {
            multiModelDialogVisible.value = true;
            multiModelEmptyVisible.value = true;
            fileList.value = [];
            recognitionResult.value = "";
          } else {
            ElMessage.warning("当前文档为只读状态，禁止编辑");
          }
        }
      },
    ]);
    const selectedValues = reactive({});  //selector更新文本所需

    const recognitionResult = ref(""); // 用于存储OCR识别结果
    const loading = ref(false);  // 设置加载状态
    const startOCR = () => {
      loading.value=true;
      // 获取上传成功的文件
      if (fileList.value.length === 0) {
        ElMessage.error("请先上传一个文件");
        return;
      }

      const file = fileList.value[0]; // 假设只上传一个文件
      const fileExtension = file.name.split('.').pop(); // 获取最后一个点号后的部分作为文件后缀
      const formData = new FormData();
      formData.append("file", file.raw); // 使用上传的文件

      const pictureExtensions = ['png', 'jpg', 'jpeg', 'pdf'];
      const audioExtensions = ['mpeg', 'wav', 'ogg', 'flac'];

      if (pictureExtensions.includes(fileExtension)) {
       // 发送文件到后端进行OCR识别
      axios
        .post("/api/chat/ocr/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          loading.value=false;
          multiModelEmptyVisible.value = false;
          recognitionResult.value = response.data.text; // 更新OCR识别结果
        })
        .catch((error) => {
          ElMessage.error("OCR失败");
        });
      }
      else if (audioExtensions.includes(fileExtension)) {
       // 发送文件到后端进行ASR识别
      axios
        .post("/api/chat/asr/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          loading.value=false;
          multiModelEmptyVisible.value = false;
          recognitionResult.value = response.data.text; // 更新识别结果
        })
        .catch((error) => {
          ElMessage.error("ASR失败");
        });
      }
      else {
        ElMessage.error('当前文件不属于任何一个可选文件类型');
      }

    };

    const insertKnowledgeRepository = () => {
      loading.value = true;
      if (fileList.value.length === 0) {
        ElMessage.error("请先上传一个文件");
        return;
      }

      const file = fileList.value[0]; // 假设只上传一个文件
      const fileName = file.name.split('.').slice(0, -1).join('.');
      const content = recognitionResult.value; // 假设内容是从 recognitionResult 中获取

      // 创建一个对象来包含 content 和 title
      const requestData = {
        content: content,
        title: fileName
      };

      const userId = localStorage.getItem("user_id");

      // 发送请求到后端
      axios
        .post(`/api/dialogue/addNewStr/${userId}/`, requestData)
        .then((response) => {
          // 处理成功响应
          ElMessage.success("数据发送成功！");
          loading.value = false;
        })
        .catch((error) => {
          // 处理错误响应
          ElMessage.error("发送数据时出错！");
          loading.value = false;
        });
    };

    // 删除后端保存的文件
    const handleClose = () =>{
      if (fileList.value.length === 0) {
        multiModelDialogVisible.value = false; // 销毁对话框
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
            multiModelDialogVisible.value = false; // 销毁对话框
        })
          .catch((error) => {
            multiModelDialogVisible.value = false; // 销毁对话框
          });
    }

    const handleRemove = (file) =>{
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
    const updateColor = (index, color) => {
      items[index].color = color;
      items[index].action(color);
    };

    // 控制排版面板的显示状态
    const formattingTemplateDiaLogVisible = ref(false);


    const formatHtmlContent = ref("");
    // 执行智能排版函数
    const formatDocument = async (cardId) => {
      // 关闭 formatting-template-dialog 对话框
      formattingTemplateDiaLogVisible.value = false;
      const formData = new FormData();
      const htmlContent = props.editor.getHTML();
      // 正则表达式匹配 id 和 data-toc-id 属性及其值
      const regex = /\s*(id|data-toc-id)="[^"]*"/g;
      // 使用正则表达式替换匹配的部分为空字符串，即删除匹配的部分
      const cleanedText = htmlContent.replace(regex, '');
      const template = ref();
      const loading = ElLoading.service({
        lock: true,
        text: '正在努力排版中...',
        background: 'rgba(255, 255, 255, 0.7)',
      });
      try {
        const response = await axios.get(`/api/user/template/${cardId}/`);
        template.value = response.data;
      } catch (error) {
        ElMessage.error("获取模板内容失败:", error);
      }

      formData.append("htmlContent", cleanedText); // 使用文档中的内容
      formData.append("templateContent", template.value.content); // 使用模板中的内容

      axios
          .post("/api/chat/format/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then(response => {
            formatHtmlContent.value = response.data.response
            props.editor.commands.clearContent()
            props.editor.commands.insertContent(formatHtmlContent.value)
          })
          .finally(() => {
            // 关闭加载
            loading.close();
          });
    }

    return {
      items,
      selectedValues,
      updateColor,
      multiModelDialogVisible,
      multiModelEmptyVisible,
      formattingTemplateDiaLogVisible,
      loading,
      beforeUpload,
      handleSuccess,
      handleExceed,
      startOCR,
      handleClose,
      handleRemove,
      fileList,
      recognitionResult,
      formatDocument,
      insertKnowledgeRepository
    };
  }
};
</script>

<style lang="scss">
.menu-item-divider {
  margin-left: 0.75rem;
  margin-right: 0.75rem;
  background-color: rgba(10, 3, 3, 0.6);
  height: 1.45rem !important;
  border-left: 0.1rem solid rgba(10, 3, 3, 0.49);
}

.color-picker {
  margin: 0 0.75rem;
  height: 1.45rem;
  width: 2rem;
  border: none;
  background: none;
  cursor: pointer;
}

.ai-multi-model-process-dialog-upload{
  width: 580px;
  height: 280px;
}

.ai-multi-model-process-dialog-card {
  text-align: left;
  width: 580px;
  height: 195px;
}
.ai-multi-model-process-dialog-card .el-card__body{
  overflow: auto;
  width: 540px;
  height: 190px;
}

.scrollable-content {
  height: 100%;
}

.ai-multi-model-process-dialog-empty{
  height: 100%;
  width: 100%;
}

.ai-multi-model-process-dialog-col{

}
.ai-multi-model-process-dialog-button{

}


</style>
