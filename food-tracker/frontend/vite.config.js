import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': process.env.VITE_PROXY_TARGET || 'http://food-tracker:8000',
      '/admin': process.env.VITE_PROXY_TARGET || 'http://food-tracker:8000',
    },
  },
  base: '/food-tracker/'
})
