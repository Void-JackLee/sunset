import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const PATH = '/sunset'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: PATH,
  server: {
    port: 8080
  },
  css: {
    preprocessorOptions: {
      scss: { api: 'modern-compiler' },
    }
  }
})
