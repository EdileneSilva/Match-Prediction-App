// vue.config.js
module.exports = {
  devServer: {
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      // Proxy API requests to avoid CORS issues in development
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/predictions': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/dashboard': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/train': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/predict': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
  
  // Build-time environment variables
  // These will be baked into the app at build time
  // Access via process.env.VUE_APP_* in your code
  css: {
    extract: true,
  },
};
