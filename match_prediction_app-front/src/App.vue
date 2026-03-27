<template>
  <div>
    <NavigationBar v-if="showNavbar" />
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
  computed: {
    showNavbar() {
      const authPages = ['landing', 'login', 'register', 'forgot-password', 'reset-password'];
      return !authPages.includes(this.$route.name);
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
 
html, body {
  height: 100%;
  width: 100%;
}
 
#app {
  font-family: 'Inter', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  width: 100%;
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