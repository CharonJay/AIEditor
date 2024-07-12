import { createApp } from 'vue'

import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/index.css'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import axios from 'axios';

import router from './router';

import 'element-plus/theme-chalk/index.css'
import 'remixicon/fonts/remixicon.css'
import 'katex/dist/katex.min.css';

import { refreshToken } from './utils/auth';

const app = createApp(App)

for (const [key, value] of Object.entries(ElementPlusIcons)) {
    app.component(key, value)
}

axios.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
        return config;
    }, error => {
        return Promise.reject(error);
});

axios.interceptors.response.use(response => {
    return response;
  },
  async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await refreshToken();
      if (newToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
        return axios(originalRequest);
      }
  }
  return Promise.reject(error);
});


app.use(ElementPlus)
app.use(router)
app.mount('#app')