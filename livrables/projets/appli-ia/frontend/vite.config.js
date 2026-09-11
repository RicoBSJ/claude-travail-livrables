import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite v8.2.2 — version relevée à npm show le 28/08/2026
// Options du proxy (target, changeOrigin) : vite.dev/config/server-options — vérifiée le 11/09/2026
// Le proxy redirige les requêtes /api/* vers le serveur Node.js (port 3000).
// Grâce au proxy, le navigateur ne voit qu'un seul serveur (Vite, port 5173)
// et n'applique pas la politique CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
})