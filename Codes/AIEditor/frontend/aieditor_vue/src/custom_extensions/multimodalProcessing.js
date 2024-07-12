import { Extension } from '@tiptap/core';
import axios from 'axios';

export default Extension.create({
  name: 'multimodalProcessing',

  addCommands() {
    return {
      // 处理图片文件
      processImage: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedImage = state.doc.textBetween(from, to, ' ');

        // 定义并调用图片处理函数
        const extractTextFromImage = (imageData, callback) => {
          let formData = new FormData();
          formData.append('image', imageData);
          let url = 'http://localhost:8000/chat/upload/'; // 访问后端接口的URL
          axios.post(url, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(res => {
            callback(res.data);
          })
          .catch(error => {
            console.error('Error processing image:', error);
          });
        };

        extractTextFromImage(selectedImage, callback);

        return true;
      },

      // 处理语音文件
      processAudio: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedAudio = state.doc.textBetween(from, to, ' ');

        // 定义并调用语音处理函数
        const extractTextFromAudio = (audioData, callback) => {
          let formData = new FormData();
          formData.append('audio', audioData);
          let url = 'http://localhost:8000/chat/extract_text_from_audio/'; // 访问后端接口的URL
          axios.post(url, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(res => {
            callback(res.data);
          })
          .catch(error => {
            console.error('Error processing audio:', error);
          });
        };

        extractTextFromAudio(selectedAudio, callback);

        return true;
      },
    };
  },
});
