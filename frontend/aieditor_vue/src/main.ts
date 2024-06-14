import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import router from '../router';

import 'element-plus/theme-chalk/index.css'
import 'remixicon/fonts/remixicon.css'
import 'katex/dist/katex.min.css';




const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')