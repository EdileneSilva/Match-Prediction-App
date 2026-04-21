import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { initSmoothScroll } from './utils/smoothScroll'

// Initialize GSAP & Lenis smooth scrolling
initSmoothScroll()

createApp(App).use(router).mount('#app')
