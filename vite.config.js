import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    // Allow any host to connect, which is required for CodeSandbox
    allowedHosts: 'all',
  },
});
