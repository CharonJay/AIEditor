<template><el-container>
    <el-table :data="files" class ="table" :row-style="{ height: '5rem', 'font-size':'1.2rem'}" :cell-style="{ padding: '0px', 'font-size': '1.2rem' }">
        <el-table-column prop="name" label="文件名">
            <template #default="{ row }">
                    <router-link class="router-link-document" :to="`/files/${row.id}`">
                        <el-icon size="32"><Document /></el-icon>
                        &nbsp;&nbsp;{{ row.name }}
                    </router-link>
            </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="上次更新">
            <template #default="{ row }">
                {{ new Date(row.updated_at).toLocaleDateString() }}
            </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建者"></el-table-column>
        <el-table-column fixed="right" label="操作" min-width="120px" align="center" width="200px">
            <template #default="{ row }">
                <el-button link @click="handleDelete(row.id)" type="primary" size="large" style="width: 50px;">删除</el-button>
                <el-button link @click="handleRename(row.id)" type="primary" size="large" style="width: 50px;">重命名</el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-dialog v-model="dialogVisible" title="重命名">
        <el-form>
            <el-form-item label="文档名称">
                <el-input v-model="filename" placeholder="重命名："></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
          <div>
            <el-button @click="dialogVisible = false">
                取消
            </el-button>
            <el-button type="primary" @click="renameFile">
                修改
            </el-button>
          </div>
        </template>
    </el-dialog>
</el-container></template>

<script setup name="CreateComponent">
import {ref, onMounted, reactive} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import axios from 'axios';
import EditorPanel from '../editor/EditorPanel.vue';


const files = ref([])
const filename = ref('')
const dialogVisible = ref(false)
const tempId = ref(0)
const router = useRouter()
const route = useRoute()

const fetchFiles = async () => {
  try {
    const response = await fetch('/api/user/filesMenu/create/' + localStorage.getItem('username') + '/')
    files.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch data:', error)
  }
}

onMounted(() => {
  fetchFiles()
})

const handleDelete = async (index) => {
  await axios.patch(`/api/user/files/updatefile/${index}/`, {
    status: 2
  })
  const response = await fetch('/api/user/filesMenu/create/' + localStorage.getItem('username') + '/')
  const data = await response.json()
  files.value = data
}

const renameFile = async () => {
  if (filename.value !== '') {
    await axios.patch(`/api/user/files/updatefile/${tempId.value}/`, {
      name: filename.value
    })
    dialogVisible.value = false
    const response = await fetch('/api/user/filesMenu/create/' + localStorage.getItem('username') + '/')
    const data = await response.json()
    files.value = data
  }
}

const handleRename = (index) => {
  dialogVisible.value = true
  tempId.value = index
}
</script>

<style scoped>
.table {
  line-height: 60px;
  font-size: 1.2rem;
  font-weight: bolder;
  margin: 1.1rem 0;
  letter-spacing: 0.1rem;
  font-family: sans-serif;
  border-radius: 10px;
}

a {
  color: #333;
  font-size: 1.2rem;
  text-decoration: none;
}
.router-link-document{
  display: flex;
  align-items: center;
  justify-items: center;
}
</style>