import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    // Explicitly allow the CodeSandbox host
    allowedHosts: ['cf9tvz-5173.csb.app'],
  },
});
