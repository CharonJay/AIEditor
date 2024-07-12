<template>
    <div class="body">
        <div class='container' ref="container">
            <div class="form-container sign-up-container">
                <!-- 注册 -->
                <el-form ref="registerForm" :model="register_form" class="register-form" :rules="registerRules">
                    <h1>用户注册</h1>
                    <el-form-item label="用户名" label-width="80px" class="form-item" prop="registerName">
                        <el-input v-model="register_form.registerName" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" label-width="80px" class="form-item" prop="registerPassword">
                        <el-input type="password" v-model="register_form.registerPassword" placeholder="请输入密码"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱" label-width="80px" class="form-item" prop="registerEmail">
                        <el-input v-model="register_form.registerEmail" placeholder="请输入邮箱"></el-input>
                    </el-form-item>
                    <el-button type="primary" @click="handleRegister">注册</el-button>
                </el-form>
            </div>
            <div class="form-container sign-in-container">
                <!-- 登陆 -->
                <el-form ref="loginForm" :model="login_form" class="login-form" :rules="loginRules">
                    <h1>用户登陆</h1>
                    <el-form-item label="用户名" label-width="80px" class="form-item" prop="loginName">
                        <el-input v-model="login_form.loginName" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" label-width="80px" class="form-item" prop="loginPassword">
                        <el-input type="password" v-model="login_form.loginPassword" placeholder="请输入密码"></el-input>
                    </el-form-item>
                    <el-button type="primary" @click="handleLogin">登陆</el-button>
                </el-form>
            </div>
            <!-- 侧边栏内容 -->
            <div class="overlay-container">
                <div class="overlay">
                    <div class="overlay-panel overlay-left">
                        <h1>智能在线编辑器</h1>
                        <h2>已有帐号？</h2>
                        <p>点我去进行登陆吧。</p>
                        <button class='ghost' @click="toSignIn">登陆</button>
                    </div>
                    <div class="overlay-panel overlay-right">
                        <h1>智能在线编辑器</h1>
                        <h2>没有帐号？</h2>
                        <p>去注册一个属于你的账号吧。</p>
                        <!-- <a href="#">忘记密码？</a> -->
                        <button class='ghost' @click="toSignUp">注册</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts" name="LoginView">
    import { ref, reactive } from 'vue'
    import { onMounted } from 'vue';
    import axios from 'axios';
    import router from '../router';

    const container = ref()
    const loginForm = ref()
    const registerForm = ref()

    onMounted(() => {
        const jwt = localStorage.getItem('jwt');
        if (jwt) {
            router.push('/space');
        }
    })

    const toSignIn = () => {
        container.value.classList.remove('right-panel-active');
    }
    const toSignUp = () => {
        container.value.classList.add('right-panel-active');
    }

    let register_form = ref({
        registerName: '',
        registerPassword: '',
        registerEmail: '',
    })
    let login_form = ref({
        loginName: '',
        loginPassword: '',
    })

    const registerRules = reactive({
        registerName: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 10, message: '用户名长度在 3 到 10 个字符', trigger: 'blur' },
        ],
        registerPassword: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' },
        ],
        registerEmail: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
        ],
    })

    const loginRules = reactive({
        loginName: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 10, message: '用户名长度在 3 到 10 个字符', trigger: 'blur' },
        ],
        loginPassword: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 16, message: '密码长度在 6 到 16 个字符', trigger: 'blur' },
        ],
    })

    const handleRegister = () => {
        registerForm.value.validate(async(valid:any) => {
            if (valid) {
                try {
                    const response = await fetch('http://127.0.0.1:8000/user/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username: register_form.value.registerName,
                            password: register_form.value.registerPassword,
                            email: register_form.value.registerEmail,
                        })
                    })
                    if (response.ok) {
                        alert('注册成功，请登录')
                        router.push('/login');
                    } else {
                        alert('注册失败，用户名或邮箱被占用')
                    }
                }catch(e){
                    console.error(e)
                }
            } else {
                console.log(valid)
                console.log('注册失败，请检查输入')
            }
        })
    }

    const handleLogin = () => {
        loginForm.value.validate(async(valid:any) => {
            if (valid) {
                try{
                    const response = await axios.post('http://127.0.0.1:8000/user/token', {
                        username: login_form.value.loginName,
                        password: login_form.value.loginPassword,
                    })
                    const accessToken = response.data.access;
                    const refreshToken = response.data.refresh;
                    const user_id = response.data.user_id;
                    localStorage.setItem('access_token', accessToken);
                    localStorage.setItem('refresh_token', refreshToken);
                    localStorage.setItem('username', login_form.value.loginName);
                    localStorage.setItem('user_id', user_id);
                    console.log('login!')
                    await router.push('/space');
                    console.log('push space!')
                }catch(e){
                    e = 'Invalid credentials. Please try again.'
                    alert('登陆失败！请检查用户名与密码')
                }
            } else {
                alert('用户名或密码错误')
            }
        })
    }
</script>

<style scoped>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    .body {
        font-family: Arial, Helvetica, sans-serif;
        background: #ffffff;
        /* background-attachment: fixed; */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0 auto;
    }
    h1 {
        margin: 0.3rem;
        font-size: 2.5rem;
    }
    h2 {
        margin: 0.3rem;
    }
    p {
        font-size: 1.3rem;
        line-height: 1.5rem;
        font-weight: 100;
        margin: 1.1rem 0;
        letter-spacing: 0.1rem;
    }
    span {
        font-size: 1rem;
        margin: 1.2rem 0;
    }
    a {
        color: #333;
        font-size: 1rem;
        text-decoration: none;
    }
    .container {
        position: relative;
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 14px 28px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22);
        padding: 0.6rem;
        width: 55rem;
        height: 35rem;
        overflow: hidden;
        max-width: 100vw;
        min-height: 70vh;
    }
    .form-container form {
        background: #fff;
        display: flex;
        flex-direction: column;
        padding: 0 1.8rem;
        height: 100%;
        justify-content: center;
        align-items: center;
    }
    .social-container {
        margin: 0.6rem 0;
    }
    .social-container a {
        border: 1px solid #eee;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin: 0 5px;
        height: 1.8rem;
        width: 1.8rem;
    }
    .social-container a:hover {
        opacity: .8;
    }
    .form-container input {
        width: 100%;
        height: 2.2rem;
        text-indent: 1rem;
        border: 1px solid #ccc;
        border-left: none;
        border-right: none;
        border-top: none;
        outline: none;
        margin: 0.6rem 0;
    }
    .form-container button:active {
        transform: scale(0.95,0.95);
    }
    .form-container button {
        padding: 0.4rem 1rem;
        background: #417dff;
        color: white;
        border: 1px solid #fff;
        outline: none;
        cursor: pointer;
        width: 5rem;
        border-radius: 8px;
        transition: all 100ms ease-in;
        margin: 0.6rem 0;
        font-size: 1rem;
        padding: 0.5rem 0;
    }
    el-form-item {
        font-size: 1rem;
    }
    .form-item {
        margin: 0.6rem 0;
    }
    .form-item label {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 0.2rem;
    }
    .form-item input {
        font-size: 1rem;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #ccc;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    .form-item input:focus {
        border-color: #417dff;
    }

    button.ghost {
        background: transparent;
        border-color: #fff;
        border: 1px solid #fff;
        outline: none;
        cursor: pointer;
        width: 5rem;
        border-radius: 8px;
        transition: all 100ms ease-in;
        margin: 0.5rem 0;
        padding: 0.5rem 0;
        color: white;
        font-size: 1rem;
    }
    button#send_code {
        width: 100%;
    }
    button.ghost:active {
        transform: scale(0.95,0.95);
    }
    .form-container {
        position: absolute;
        top: 0;
        height: 100%;
        transition: all 0.5s ease-in;
    }
    .sign-in-container {
        left: 0;
        width: 50%;
        z-index: 2;
    }
    .sign-up-container {
        left: 0;
        width: 50%;
        opacity: 0;
        z-index: 1;
    }
    .overlay {
        background: #417dff;
        width: 200%;
        height: 100%;
        position: relative;
        left: -100%;
        transition: all 0.6s ease-in-out;
        color: white;
    }
    .overlay-container {
        position: absolute;
        top: 0;
        right: 0;
        width: 50%;
        height: 100%;
        overflow: hidden;
        transition: all 0.6s ease-in-out;
        z-index: 99;
    }
    .overlay-panel {
        position: absolute;
        top: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 50%;
        height: 100%;
        padding: 0 2.2rem;
    }
    .overlay-right {
        right: 0;
    }
    .container.right-panel-active .overlay-container {
        transform: translateX(-100%);
    }
    .container.right-panel-active .sign-in-container {
        transform: translateX(100%);
    }
    .container.right-panel-active .sign-up-container {
        transform: translateX(100%);
        opacity: 1;
        z-index: 5;
        transition: all 0.6s ease-in-out;
    }
    .container.right-panel-active .overlay {
        transform: translateX(50%);
    }
    .container.right-panel-active .overlay-left {
        transform: translateX(0);
        transition: all 0.6s ease-in-out;
    }
    .container.right-panel-active .overlay-right {
        transform: translateX(20%);
        transition: all 0.6s ease-in-out;
    }
</style>
