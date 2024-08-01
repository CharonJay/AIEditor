<template>
    <div>
    <el-header class="page-header">
        <h1 class="LOGO">文心一编</h1>
        <p style="margin-left: auto">用户：{{ username }}&nbsp;&nbsp;</p>
        <el-dropdown @command="handleCommand">
            <span>
                <el-avatar class="user-avatar" shape="square" size="" :src='avatar'></el-avatar>
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="personalCenter">个人中心</el-dropdown-item>
                    <el-dropdown-item command="logout">退出登陆</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </el-header>
    <el-container class="body">
        <el-main class="my-main">
        <el-container>
            <el-aside class="aside">
                <div class="create-doc">
                    <h2>欢迎</h2>
                </div>
                <div class="create-button">
                <el-button @click="handdleCreate" type="primary" style="width: 100%;height: 100%; font-family: sans-serif; font-weight: bolder; font-size: 1.3rem;">
                    创建文档
                </el-button>
                </div>
                <div class="create-button">
                <el-button @click="handleShare" type="primary" style="width: 100%;height: 100%; font-family: sans-serif; font-weight: bolder; font-size: 1.3rem;">
                    加入文档
                </el-button>
                </div>
                <el-menu class="custom-menu" :default-active="activeIndex" @select="handleSelect">
                    <el-divider />
                    <el-menu-item index="create" class="aside-menu-item">
                        <el-icon size="32"><Document /></el-icon><p>&nbsp;&nbsp;我创建的</p>
                    </el-menu-item>
                    <el-menu-item index="trash" class="aside-menu-item">
                        <el-icon size="32"><DeleteFilled /></el-icon><p>&nbsp;&nbsp;回收站</p>
                    </el-menu-item>
                    <el-divider />
                </el-menu>
            </el-aside>
            <el-container style="min-width: 600px;" class="container">
                <el-header class="header">
                    <p>{{ currentName }}</p>
                </el-header>
                <el-main class="main-table">
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
                <el-form-item>
                    <el-radio-group v-model="radio" class="ml-4">
                        <el-radio label="0" size="large">单人文档</el-radio>
                        <el-radio label="1" size="large">协作文档</el-radio>
                    </el-radio-group>
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
        <el-dialog v-model="shareVisible" title="加入文档">
            <el-form>
                <el-form-item label="邀请码">
                    <el-input v-model="inviteCode" placeholder="请输入邀请码"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div>
                    <el-button @click="shareVisible = false">
                        取消
                    </el-button>
                    <el-button type="primary" @click="toShareDocument">
                        加入
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </el-container>
    </div>
</template>

<script lang="ts", name="Space">
import { useRouter } from 'vue-router';
import TrashComponent from '@/components/space/TrashComponent.vue';
import CreateComponent from '@/components/space/CreateComponent.vue';
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
        const shareVisible = ref(false)
        const radio = ref('0')
        const inviteCode = ref('')

        const logout = () => {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('username');
            localStorage.removeItem('password');
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
                  status: radio.value
                })
                dialogVisible.value = false
                window.location.reload()
            }
        }
        const avatar = ref('')
        onMounted(async () => {
            currentComponent.value = 'CreateComponent'
            try {
                const response = await axios.get(`/api/user/users/${localStorage.getItem('user_id')}/`)
                if (response.data.avatar) {
                    avatar.value = response.data.avatar
                }
                else {
                    avatar.value = 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png'
                }
            }
            catch (error) {
                console.log('用户头像加载失败')
            }
        })

        const handleCommand = (command: string) => {
            switch (command) {
                case 'personalCenter':
                    console.log('personalCenter!')
                    router.push('/personalcenter')
                    break
                case 'logout':
                    console.log('logout!')
                    logout()
                    break
            }
        }

        const handleShare = () => {
            shareVisible.value = true
        }
        const toShareDocument = ()=> {
            if (inviteCode.value !== '') {
                const decoded = atob(inviteCode.value)
                const [tempname, _] = decoded.split(',')
                const decodedId = tempname.match(/document(\d+)/)![1];
                console.log(inviteCode)
                console.log(decodedId)
                router.push(`/files/${decodedId}/${1}`)
            }
        }

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
            activeIndex,
            handleSelect,
            currentName,
            handdleCreate,
            dialogVisible,
            filename,
            createDocument,
            handleCommand,
            avatar,
            radio,
            handleShare,
            shareVisible,
            inviteCode,
            toShareDocument
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
      height: 5vh;
    }
    .body{
      height: 93vh;
    }
    .LOGO {
      height: 100%;
      font-size: 30px;
      font-family: sans-serif;
      margin-left: 30px; /* 调整此值以设置所需的右移距离 */
    }
    .el-dropdown-item{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .aside {
      width: 200px;
      min-height: 88vh;
      background-color: rgba(255, 255, 255, 0.8);
      border: 1px solid #9bcfff;
      margin-right: 20px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
              0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
              -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
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
      margin-bottom: 0px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
              0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
              -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
    }
    .my-main {
        background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
        margin-top: 1px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
    }
    .main-table {
        background-color: #ffffff;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
              0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
              -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
    }
    ::v-deep .el-menu-item.is-active {
        background-color: #c3ecff !important; /* 修改背景颜色 */
        color: #36a4fe !important; /* 修改字体颜色 */
    }
    .custom-menu {
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
    .user-avatar{
       cursor: pointer;
    }
    .create-button{
      height: 5rem;
      margin: 20px 5px;
    }
</style>