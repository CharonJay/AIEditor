import { Extension } from '@tiptap/core';
import axios from 'axios';

export default Extension.create({
  name: 'textEnhancements',

  addCommands() {
    return {
      // ai摘要功能
      summaryText: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedText = state.doc.textBetween(from, to, ' ');

        // 定义并调用摘要函数
        const summary = (text, callback) => {
          let url = 'http://localhost:8000/chat/getsummary/'; // 访问后端接口的url
          axios.post(url, { message: text.trim() })
            .then(res => {
              callback(res.data);
            })
            .catch(error => {
              console.error('Error polishing text:', error);
            });
        };

        summary(selectedText, callback);

        return true;
      },

      // ai润色功能
      polishText: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedText = state.doc.textBetween(from, to, ' ');

        // 定义并调用润色函数
        const polish = (text, callback) => {
          let formData = new FormData();
          formData.append('message', text.trim());
          let url = 'http://localhost:8000/chat/getpolish/'; // 访问后端接口的url
          axios.post(url, { message: text.trim() })
            .then(res => {
              callback(res.data);
            })
            .catch(error => {
              console.error('Error polishing text:', error);
            });
        };

        polish(selectedText, callback);

        return true;
      },
      // ai续写功能
      continuationText: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedText = state.doc.textBetween(from, to, ' ');

        // 定义并调用续写函数
        const continuation = (text, callback) => {
          let formData = new FormData();
          formData.append('message', text.trim());
          let url = 'http://localhost:8000/chat/getcontinuation/'; // 访问后端接口的url
          axios.post(url, { message: text.trim() })
            .then(res => {
              callback(res.data);
            })
            .catch(error => {
              console.error('Error continuing text:', error);
            });
        };

        continuation(selectedText, callback);

        return true;
      },
      // ai纠错功能
      correctText: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedText = state.doc.textBetween(from, to, ' ');

        // 定义并调用纠错函数
        const correct = (text, callback) => {
          let formData = new FormData();
          formData.append('message', text.trim());
          let url = 'http://localhost:8000/chat/getcorrection/'; // 访问后端接口的url
          axios.post(url, { message: text.trim() })
            .then(res => {
              callback(res.data);
            })
            .catch(error => {
              console.error('Error continuing text:', error);
            });
        };

        correct(selectedText, callback);

        return true;
      },
      //ai翻译功能
      translateText: (callback) => ({ state, dispatch }) => {
        const { from, to } = state.selection;
        const selectedText = state.doc.textBetween(from, to, ' ');

        // 定义并调用翻译函数
        const translate = (text, callback) => {
          let formData = new FormData();
          formData.append('message', text.trim());
          let url = 'http://localhost:8000/chat/gettranslation/'; // 访问后端接口的url
          axios.post(url, { message: text.trim() })
            .then(res => {
              callback(res.data);
            })
            .catch(error => {
              console.error('Error continuing text:', error);
            });
        };

        translate(selectedText, callback);

        return true;
      },
    };
  },
});
