<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>{{ title }}</span>
        <el-dropdown class="drop-down-knowledge-repository" trigger="click">
          <span class="el-dropdown-link">
            更多
            <el-icon class="el-icon--right">
              <arrow-down />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handlePreview">预览</el-dropdown-item>
              <el-dropdown-item @click="handleDelete">删除</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </template>
    <div>{{ content }}</div>
    <div class="knowledgeCardDialog">
      <el-dialog
        v-model="knowledgeCardDialogVisible"
        :title=title
        width="900"
        :before-close="handleClose"
      >
        {{content}}
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="knowledgeCardDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="knowledgeCardDialogVisible = false">
              确认
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>

  </el-card>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { ArrowDown } from '@element-plus/icons-vue';
import {ElMessage, ElMessageBox, ElMessageBoxOptions} from 'element-plus';
import axios from "axios";

export default defineComponent({
  name: 'KnowledgeRepositoryCard',
  components: { ArrowDown },
  props: {
    title: {
      type: String,
      required: true,
    },
    content: {
      type: String,
      required: true,
    },
  },
  setup(props, context) {
    const knowledgeCardDialogVisible = ref(false);

    const handleRename = () => {
      const options: ElMessageBoxOptions = {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      };
      ElMessageBox.prompt('请输入新的名称', '重命名', options)
        .then(({ value }) => {
          console.log('新名称:', value);
        })
        .catch(() => {
          console.log('取消重命名');
        });
    };

      const handleDelete = () => {
        const options: ElMessageBoxOptions = {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        };

        ElMessageBox.confirm('确定要删除吗?', '警告', options)
          .then(async () => {
            const userId = localStorage.getItem("user_id");
            const requestData = {
              name: props.title  // Adjusted to match backend's expected 'name' field
            };

            axios
              .post(`/api/dialogue/deleteDocument/${userId}/`, JSON.stringify(requestData), {
                headers: {
                  'Content-Type': 'application/json'
                }
              })
              .then((response) => {
                // Handle successful response
                ElMessage.success("知识删除成功！");
                context.emit('documentDeleted');
              })
              .catch((error) => {
                // Handle error response
                ElMessage.error("知识删除失败！");
              });
          })
          .catch(() => {
            // Handle cancel or dismiss
            ElMessage.info('取消删除操作');
          });
      };


    const handlePreview = () => {
      knowledgeCardDialogVisible.value = true;
    };

    const handleClose = (done: () => void) => {
      done();
    };

    return {
      knowledgeCardDialogVisible,
      handleRename,
      handleDelete,
      handlePreview,
      handleClose,
    };
  },
});
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drop-down-knowledge-repository {
  cursor: pointer;
}


.knowledgeCardDialog {
  ::v-deep .el-dialog {
    height: auto;
    max-height: 80vh;
    overflow: hidden;

    .el-dialog__body {
      text-align: left;
      max-height: 50vh!important;
      overflow-y: auto;
    }
  }
}

</style>
