<template>
  <div>
    <NavigationBar v-if="showNavbar" />
    <router-view/>
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
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  width: 100%;
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