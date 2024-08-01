import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    host: '127.0.0.1',
    port: 8000,
    proxy: {
        '/api': {
            target: 'http://6484ccf8.r3.cpolar.cn',
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/api/, '')
        }
    }
  }
})

