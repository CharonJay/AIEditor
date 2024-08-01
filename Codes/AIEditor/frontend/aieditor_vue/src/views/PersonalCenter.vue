<template class="personal-center">
    <el-page-header class="header" @back="goBack" :icon="ArrowLeft" content="个人信息" />
    <div class="body">
    <el-container>
        <el-aside class="left-container">
            <el-avatar shape="square" :src="userInfo.avatar" :size="150" style="margin-top: 20px;"></el-avatar>
            <div class="info">
                <h1>{{ userInfo.username }}</h1>
                <p style="font-size: 18px;"><strong>{{ userInfo.email }}</strong></p>
            </div>
            <el-tooltip content="成为会员，可以使用文心一言4.0的全部功能!" placement="top" style="font-size: 1.5rem;">
            <div v-if="userInfo.is_member">
                <p style="font-size: 18px;"><strong>您已成为会员</strong></p>
            </div>
            <div v-else>
                <el-button type="primary" @click="handlePayment">成为会员</el-button>
            </div>
            </el-tooltip>
        </el-aside>
        <el-main class="right-container">
            <el-card class="personal-info">
                <template #header>
                    <span>个人信息</span>
                </template>
                <el-form :model="userInfo" label-width="150px">
                    <el-form-item label-width="150px" label="头像" style="display: flex; justify-content: center; align-items: center;">
                        <el-tooltip content="点击更换头像" placement="top">
                            <el-upload
                                action="/api/user/upload_avatar/"
                                :headers="{ Authorization: `Bearer ${accessToken}` }"
                                :show-file-list="false"
                                :on-success="handleAvatarUpload"
                                accept="image/*"
                                >
                                <el-avatar :src="userInfo.avatar" shape="square" size="large" style="margin-left: 20px;">
                                    <i class="el-icon-plus"></i>
                                </el-avatar>
                            </el-upload>
                        </el-tooltip>
                    </el-form-item>

                    <el-form-item style="margin-top: 30px" label="真实姓名">
                        <div style="display: flex;">
                            <el-input v-model="userInfo.firstname" :disabled="!editing" placeholder="姓"  style="width: 8rem; margin-left: 20px;"></el-input>
                            <el-input v-model="userInfo.lastname" :disabled="!editing" placeholder="名"  style="width: 8rem; margin-left: 20px"></el-input>
                        </div>
                    </el-form-item>

                    <el-form-item style="margin-top: 30px" label="邮箱">
                        <el-input v-model="userInfo.email" :disabled="!editing" style="width: 40rem; margin-left: 20px;"></el-input>
                    </el-form-item>

                    <el-form-item style="margin-top: 30px" label="个人介绍">
                        <el-input type="textarea" :rows="5" v-model="userInfo.information" :disabled="!editing" style="margin-left: 20px; width: 40rem; "></el-input>
                    </el-form-item>

                    <el-form-item style="margin-top: 50px">
                        <el-button type="primary" @click="editProfile">{{ editing ? '保存' : '编辑' }}</el-button>
                        <el-button v-if="editing" @click="cancelEdit">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-main>
    </el-container>
</div></template>
  
<script setup name="PersonalCenter">
    import { ref, reactive, onMounted } from 'vue' 
    import { ArrowLeft } from '@element-plus/icons-vue'
    import { useRouter } from 'vue-router'
    import axios from 'axios'
    import { ElMessage } from 'element-plus'
    import { useRoute } from 'vue-router'

    const router = useRouter()
    const editing = ref(false)
    const data = ref()
    const dialogVisible = ref(false)
    const userInfo = reactive({
        username: '',
        email: '',
        information: '',
        avatar: '',
        firstname: '',
        lastname: '',
        password: ''
    })

    const accessToken = localStorage.getItem('access_token')
    const handleAvatarUpload = (response) => {
        console.log(response)
        if (response.data && response.data.avatar) {
            userInfo.avatar = response.data.avatar
            ElMessage.success('上传成功')
        }
    }

    const getUserData = async () => {
        const response = await axios.get(`/api/user/users/${localStorage.getItem('user_id')}/`)
        userInfo.username = localStorage.getItem('username')
        userInfo.password = localStorage.getItem('password')
        userInfo.email = response.data.email
        userInfo.information = response.data.information
        userInfo.firstname = response.data.first_name
        userInfo.lastname = response.data.last_name
        userInfo.is_member = response.data.is_member
        if (!response.data.avatar) {
            userInfo.avatar = 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png'
        }
        else {
            userInfo.avatar = response.data.avatar
        }
        console.log(userInfo)
    }

    // -----会员----
    let loading = true
    let payFailError = false
    
    const handlePayment = async() => {
        try {
            const response = await axios.post(`/api/member/create-alipay-payment/${localStorage.getItem('user_id')}/`, {}, {
            maxRedirects: 0, // 禁用axios自动重定向
            validateStatus: function (status) {
                return status >= 200 && status < 400; // 接受2xx和3xx状态码
            }
            });

            if (response.status === 303 && response.data.url) {
            window.location.href = response.data.url; // Redirect to Alipay for payment
            } else {
                payFailError = 'Unexpected response, please try again.';
            }
        }
        catch(error) {
            payFailError = 'Payment failed, please try again.';
            loading = false;
        } finally {
            loading = false;
        }
    }


    onMounted(()=>{
        getUserData()
        const route = useRoute();
        const status = route.query.status;

        if (status) {
        dialogVisible.value = true;
        if (status === 'success') {
            console.log('Payment success')
        } else if (status === 'failure') {
            console.log('Payment failure')
        }
        }
    })

    const originalUserInfo = reactive({})
    const editProfile = async() => {
        if (editing.value) {
            try {
                await axios.patch(`/api/user/users/${localStorage.getItem('user_id')}/`, {
                    username: userInfo.username,
                    email: userInfo.email,
                    information: userInfo.information,
                    first_name: userInfo.firstname,
                    last_name: userInfo.lastname,
                    password: userInfo.password,
                    // avatar: userInfo.avatar,
                    is_active: true
                })
                ElMessage.success('上传成功')
            }catch(error) {
                ElMessage.error('更新失败，请检查输入内容')
            }
        } else {
            originalUserInfo.value = { ...userInfo.value }
        }
        editing.value = !editing.value
    }


    
    const cancelEdit = () => {
        // Restore the original data
        // userInfo.value = { ...originalUserInfo.value }
        editing.value = false
    }
    const togglePassword = () => {
        showPassword.value = !showPassword.value
    }
    const editAvatar = () => {
        console.log('Edit avatar')
    }
    const goBack = () => {
        router.push('/space')
    }
</script>

<style scoped>
h1 {
    font-size: 2.5rem;
}
.body {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
    height: 95vh;
}
.el-tooltip__popper{
    font-size: 1.5rem
}
.header {
    font-size: 25px;
    font-family: sans-serif;
    background-color: rgba(255, 255, 255, 0);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 底部和右侧阴影 */
}
.left-container {
    width: 17vw;
    height: 90vh;
    margin-top: 20px;
    margin-left: 20px;
    background-color: rgba(255, 255, 255, 0.7);

    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
              0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
              -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
    margin-right: 20px;
}
.right-container{
    width: 17vw;
    height: 95vh;

}
.personal-info {
    height: 99%;
    width: 98%;
    margin-right: 10px;
    background-color: rgba(255, 255, 255, 0.7);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
            0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
            -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
}
.el-card *{
    font-size: 1.2rem;
    font-weight: 600;
    font-family: sans-serif;
}
.el-card{
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), /* 底部和右侧阴影 */
              0 -2px 4px rgba(0, 0, 0, 0.1), /* 顶部阴影 */
              -2px 0 4px rgba(0, 0, 0, 0.1); /* 左侧阴影 */
}

p {
    line-height: 30px;
    font-size: 1.3rem;
    font-weight: bolder;
    font-family: sans-serif;
}

</style>