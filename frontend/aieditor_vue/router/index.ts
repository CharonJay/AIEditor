import { createRouter, createWebHistory } from 'vue-router';
import Chat from '../src/components/Chat.vue'; // 聊天界面组件

const routes = [
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
