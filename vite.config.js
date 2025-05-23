import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode,process.cwd())
  console.log(env)
  return {
    plugins: [vue()],
    base: env.VITE_BASE,
    server: {
      port: 8080
    },
    css: {
      preprocessorOptions: {
        scss: { api: 'modern-compiler' },
      }
    }
  }
})
