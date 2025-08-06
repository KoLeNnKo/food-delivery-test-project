export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  # FastAPI-бэкенд
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})