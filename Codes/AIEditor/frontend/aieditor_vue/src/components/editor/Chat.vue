<template>
    <div class="chat-box">
      <div class="overlay">
        <h1>文心一言</h1>
        <div>
          使用知识库
          <el-switch
            v-model="useKnowledge"
            class="mb-2"
            style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
            inline-prompt
            active-text="Y"
            inactive-text="N"
          />
        </div>
      </div>
      <div class="messages">
        <el-scrollbar height="100%">
          <div v-for="message in messages" :key="message.id" :class="['message', message.person === 'admin' ? 'right' : 'left']">
            <div class="message-content">
              {{ message.say }}
            </div>
          </div>
          <div v-if="isLoading" class="loading-message">加载中...</div>
        </el-scrollbar>
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
      useKnowledge: false,
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

      if (this.useKnowledge){
        axios.post(`/api/dialogue/dialogue/${localStorage.getItem('user_id')}/`, { message: this.userInput.trim() })
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
      }else {
        axios.post(`/api/dialogue/dialogue/${localStorage.getItem('user_id')}/`, { message: this.userInput.trim() })
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
      }


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

<style scoped>
.overlay {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 30px;
  background-color: rgba(255, 255, 255, 0.8); /* 半透明背景色 */
  padding: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}
</style>
