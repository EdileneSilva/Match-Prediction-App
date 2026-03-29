<template>
  <nav class="navbar">
    <div class="nav-brand">
      <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
    </div>
    <div class="nav-menu">
      <template v-if="isAuthenticated">
        <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
        <router-link to="/predictions" class="nav-item">Prédictions</router-link>
        <router-link to="/history" class="nav-item">Historique</router-link>
        <router-link to="/profile" class="nav-item">Profil</router-link>
        <router-link to="/exit" class="nav-item exit">Déconnexion</router-link>
      </template>
      <template v-else>
        <router-link to="/login" class="nav-item">Se connecter</router-link>
        <router-link to="/register" class="nav-item register-btn">Créer un compte</router-link>
      </template>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavigationBar",
  data() {
    return {
      isAuthenticated: !!localStorage.getItem('token')
    };
  },
  watch: {
    $route() {
      this.isAuthenticated = !!localStorage.getItem('token');
    }
  }
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 0.8rem 2.5rem;
  border-bottom: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.nav-brand {
  display: flex;
  align-items: center;
}

.logo-img {
  height: 3.5rem;
  width: auto;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.2));
  transition: transform 0.3s ease;
}

.logo-img:hover {
  transform: scale(1.05);
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-item {
  color: var(--text-primary);
  text-decoration: none;
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  position: relative;
  letter-spacing: 0.5px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--accent-secondary);
  transform: translateY(-2px);
}

.nav-item.router-link-active {
  color: var(--accent-secondary);
  background: rgba(0, 212, 255, 0.08);
}

.nav-item.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: var(--accent-secondary);
  border-radius: 10px;
  box-shadow: 0 0 10px var(--accent-secondary);
}

.nav-item.exit {
  background: rgba(248, 113, 113, 0.1);
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.2);
  margin-left: 0.5rem;
}

.nav-item.exit:hover {
  background: #f87171;
  color: white;
  border-color: #f87171;
  box-shadow: 0 0 15px rgba(248, 113, 113, 0.4);
}

.nav-item.register-btn {
  background: var(--accent-gradient);
  color: white;
  margin-left: 0.5rem;
  box-shadow: 0 4px 15px rgba(224, 38, 255, 0.2);
}

.nav-item.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(224, 38, 255, 0.4);
}

@media (max-width: 768px) {
  .navbar {
    padding: 0.8rem 1.5rem;
  }

  .nav-menu {
    gap: 0.5rem;
  }

  .nav-item {
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
  }
}

</style>
