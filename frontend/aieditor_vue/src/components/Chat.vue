<template>
    <div class="chat-box">
      <div class="messages">
        <div v-for="message in messages" :key="message.id" :class="['message', message.person === 'admin' ? 'right' : 'left']">
          <div class="message-content">
            {{ message.say }}
          </div>
        </div>
        <div v-if="isLoading" class="loading-message">加载中...</div>
      </div>
      <div class="input-area">
        <textarea v-model="userInput" placeholder="请输入内容" @keydown="handleKeydown" rows="3"></textarea>
        <button @click="sendQuestion">发送</button>
      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userInput: '',
      messages: [
        { id: 1, person: 'mechanical', say: '你好，有什么可以帮到你呢？'}
      ],
      isLoading: false,
    };
  },
  methods: {
    sendQuestion() {
      if (!this.userInput.trim()) {
        alert('请输入内容');
        return;
      }
      this.isLoading = true;
      const newMessage = {
        id: Date.now(),
        person: 'admin',
        say: this.userInput.trim(),

      };
      this.messages.push(newMessage);

      axios.post('http://localhost:8000/chat/chat/', { message: this.userInput.trim() })
        .then(response => {
          this.messages.push({
            id: Date.now(),
            person: 'mechanical',
            say: response.data.response,

          });
        })
        .catch(error => {
          console.error('Error:', error);
          this.messages.push({
            id: Date.now(),
            person: 'mechanical',
            say: '抱歉，无法获取回答。',

          });
        })
        .finally(() => {
          this.isLoading = false;
        });
      this.userInput = '';
    },
    handleKeydown(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        if (this.userInput.trim()) {
          this.sendQuestion();
        }
      }
    }
  }
};
</script>
