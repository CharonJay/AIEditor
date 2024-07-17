import { createRouter, createWebHistory } from 'vue-router';
import Chat from '@/components/editor/Chat.vue'; // 聊天界面组件
import Space from '@/views/Space.vue'; // 个人中心组件
import LoginView from "@/views/LoginView.vue";
import EditorPanel from '@/components/editor/EditorPanel.vue';


const routes = [
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView,
  },
  {
    path: "/space",
    name: "Space",
    component: Space,
  },
  {
    path: "/editor",
    name: "EditorPanel",
    component: EditorPanel,
  },
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: '/files/:id',
    name: 'File',
    component: EditorPanel,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, _from, next) => {
  console.log('Navigating to:', to.path)
  console.log('Available routes:', router.getRoutes())
  next()
})

export default router;
