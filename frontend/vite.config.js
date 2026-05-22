import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  base: '/DEAL/',
  server: {
    host: true,
    port: 5173,
  },
});
