<template>
  <div :class="{ 'dark-mode': isDarkMode }" class="app-wrapper">
    <div class="app-bg-nebula"></div>
    <NavigationBar v-if="showNavbar" />
    <button class="theme-toggle" @click="toggleTheme" title="Changer le thème">
      <span v-if="isDarkMode">☀️</span>
      <span v-else>🌙</span>
    </button>
    <router-view v-slot="{ Component, route }">
      <transition :name="route.meta.transition || 'fade'" mode="out-in">
        <component :is="Component" :key="route.path" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'

export default {
  components: {
    NavigationBar
  },
  data() {
    return {
      isDarkMode: false
    }
  },
  created() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      this.isDarkMode = savedTheme === 'dark';
    } else {
      // Default to dark mode based on premium design requested
      this.isDarkMode = true;
    }
    this.applyTheme();
  },
  computed: {
    showNavbar() {
      const authPages = ['landing', 'login', 'register', 'forgot-password', 'reset-password'];
      return !authPages.includes(this.$route.name);
    }
  },
  methods: {
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
      this.applyTheme();
    },
    applyTheme() {
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark-mode');
      } else {
        document.documentElement.classList.remove('dark-mode');
      }
    }
  }
}
</script>

<style>
:root {
  --bg-color: #05070a;
  --bg-cosmic: radial-gradient(circle at 50% 50%, #1a0b2e 0%, #05070a 100%);
  --text-primary: #ffffff;
  --text-secondary: #a0aec0;
  --glass-bg: rgba(13, 15, 26, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-hover: rgba(13, 15, 26, 0.9);
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
  --accent-primary: #e026ff; /* Magenta */
  --accent-secondary: #00d4ff; /* Cyan */
  --accent-gradient: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
}

:root.dark-mode {
  --bg-color: #05070a;
  --bg-cosmic: radial-gradient(circle at 50% 50%, #1a0b2e 0%, #05070a 100%);
  --text-primary: #ffffff;
  --text-secondary: #a0aec0;
  --glass-bg: rgba(13, 15, 26, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-hover: rgba(13, 15, 26, 0.9);
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
  --accent-primary: #e026ff;
  --accent-secondary: #00d4ff;
  --accent-gradient: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
}

/* Global Fix for SplitType + Background-Clip Text */
.text-highlight, 
h1 span, 
h2 span,
h2 span.highlight {
  display: inline-block !important;
  background: var(--accent-gradient);
  -webkit-background-clip: text !important;
  background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  color: var(--accent-secondary) !important; /* Fallback for older browsers */
  position: relative;
  z-index: 10;
}

/* Ensure children split by SplitType also inherit the clipping */
.text-highlight .word,
.text-highlight .char,
h1 span .word,
h1 span .char,
h2 span .word,
h2 span .char,
h2 span.highlight .word,
h2 span.highlight .char {
  background: inherit !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  color: inherit !important;
  display: inline-block !important;
}


* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
 
html, body {
  min-height: 100%;
  background: var(--bg-cosmic);
  background-attachment: fixed;
  color: var(--text-primary);
  transition: background 0.5s ease, color 0.5s ease;
  overflow-x: hidden;
}


.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.theme-toggle {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  color: var(--text-primary);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 9999;
  box-shadow: 0 4px 15px var(--glass-shadow);
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  transform: scale(1.1);
  background: var(--glass-hover);
}
 
#app {
  font-family: 'Inter', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  position: relative;
}

.app-bg-nebula {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/cosmic-nebula.png");
  background-size: cover;
  background-position: center;
  opacity: 0.1; /* Reduced opacity for a more subtle effect */
  pointer-events: none;
  z-index: -1;
}

/* Page Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s ease-out;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
}
.scale-enter-from {
  opacity: 0;
  transform: scale(0.95);
}
.scale-leave-to {
  opacity: 0;
  transform: scale(1.05);
}
 
nav {
  padding: 30px;
}
 
nav a {
  font-weight: bold;
  color: #2c3e50;
}
 
nav a.router-link-exact-active {
  color: #42b983;
}
</style>