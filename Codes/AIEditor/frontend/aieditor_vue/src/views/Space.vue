<template>
  <el-header class="page-header">
    <h1 class="LOGO">文心一编</h1>
  </el-header>
<el-container class="body">

    <el-main class="my-main">
      <el-container>
        <el-aside class="aside">
            <div class="create-doc">
                <h2>你好! {{ username }}</h2>
            </div>
            <div class="create-button">
              <el-button @click="handdleCreate" type="primary" style="width: 100%;height: 100%; font-family: sans-serif; font-weight: bolder; font-size: 1.3rem;">
                  创建文档
              </el-button>
            </div>
            <el-menu class="custom-menu" :default-active="activeIndex" @select="handleSelect">
                <el-divider></el-divider>
                <el-menu-item index="create">
                    <el-icon size="32"><Document /></el-icon><p>&nbsp;&nbsp;我创建的</p>
                </el-menu-item>
                <el-menu-item index="trash">
                    <el-icon size="32"><DeleteFilled /></el-icon><p>&nbsp;&nbsp;回收站</p>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-container style="min-width: 600px;" class="container">
            <el-header class="header">
                <p>{{ currentName }}</p>
                <el-button type="danger" @click="logout">退出登陆?</el-button>
            </el-header>
            <el-main class="table">
                <component :is="currentComponent"></component>
            </el-main>
        </el-container>
      </el-container>
    </el-main>
    <el-dialog v-model="dialogVisible" title="创建文档">
        <el-form>
            <el-form-item label="文档名称">
                <el-input v-model="filename" placeholder="请输入文档名称"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <div>
                <el-button @click="dialogVisible = false">
                    取消
                </el-button>
                <el-button type="primary" @click="createDocument">
                    创建
                </el-button>
            </div>
        </template>
    </el-dialog>
</el-container>
</template>

<script lang="ts", name="Space">
import { useRouter } from 'vue-router';
// import AllFilesComponent from '../components/space/AllFilesComponent.vue';
import TrashComponent from '../components/space/TrashComponent.vue';
// import ShareComponent from '../components/space/ShareComponent.vue';
import CreateComponent from '../components/space/CreateComponent.vue';
import { onMounted } from 'vue';
import { ref } from 'vue'
import axios from 'axios';
import {DocumentAdd} from "@element-plus/icons-vue";

export default {
    components: {
      DocumentAdd,
        TrashComponent,
        CreateComponent
    },
    setup(){
        const username = localStorage.getItem('username')
        const router = useRouter()
        const currentComponent = ref('allfiles')
        let activeIndex = ref('AllFilesComponents')
        const currentName = ref('我创建的')
        const dialogVisible = ref(false)

        const logout = () => {
            console.log('logout')
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('username');
            localStorage.removeItem('user_id');
            router.push('/login')
        }

        const handdleCreate = () => {
            dialogVisible.value = true
        }

        const filename = ref('')

        const createDocument = async() => {
            if (filename.value !== '') {
                console.log('Create!')
                await axios.post('/api/user/files/createfile/', {
                  name: filename.value,
                  creator: username,
                  status: 0
                })
                dialogVisible.value = false
                window.location.reload()
            }
        }

        onMounted(() => {
            currentComponent.value = 'CreateComponent'
        })

        const handleSelect = (index: string) => {
            switch (index) {
                // case 'allfiles':
                //     currentComponent.value = 'AllFilesComponent'
                //     currentName.value = '所有文件'
                //     break
                case 'create':
                    currentComponent.value = 'CreateComponent'
                    currentName.value = '我创建的'
                    break
                case 'trash':
                    currentComponent.value = 'TrashComponent'
                    currentName.value = '回收站'
                    break
                // case 'share':
                //     currentComponent.value ='ShareComponent'
                //     currentName.value = '分享给我'
                //     break
                default:
                    currentComponent.value ='CreateComponent'
                    break
            }
            activeIndex.value = index
        }
        return {
            username,
            currentComponent,
            logout,
            activeIndex,
            handleSelect,
            currentName,
            handdleCreate,
            dialogVisible,
            filename,
            createDocument
        }
    }
}
</script>

<style scoped>
    .page-header{
      display: flex;
      justify-content: flex-start;
      align-items: center;
      background: #417dff;
      color: white;
    }
    .body{
      height: 98vh;
    }
    .LOGO {
      height: 100%;
      font-size: 30px;
      font-family: sans-serif;
      margin-left: 30px; /* 调整此值以设置所需的右移距离 */
    }
    .aside {
      width: 200px;
      min-height: 88vh;
      background-color: #ffffff;
      border: 1px solid #9bcfff;
      box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
      margin-right: 5px;
    }
    .create-doc {
      height: 60px;
      line-height: 60px;
      background-color: #122778;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .header {
      background-color: #e5f2ff;
      margin-bottom: 5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .my-main {
        background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
        margin-top: 5px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
    }
    .table {
        background-color: #ffffff;
    }
    ::v-deep .el-menu-item.is-active {
        background-color: #c3ecff !important; /* 修改背景颜色 */
        color: #36a4fe !important; /* 修改字体颜色 */
    }
    .custom-menu {
        background-color:#ffffff;
        margin: 20px 5px;
        border: none;
    }
    h1 {
        margin: 0.3rem;
        font-size: 2rem;
    }
    h2 {
        margin: 0.3rem;
    }
    p {
        line-height: 60px;
        font-size: 1.3rem;
        font-weight: bolder;
        margin: 1.1rem 0;
        letter-spacing: 0.1rem;
        font-family: sans-serif;
    }
    .create-button{
      height: 5rem;
      margin: 20px 5px;
    }
</style>