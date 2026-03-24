<template>
  <nav class="navbar">
    <div class="nav-brand">
      <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
    </div>
    <div class="nav-menu">
      <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
      <router-link to="/predictions" class="nav-item">Prédictions</router-link>
      <router-link to="/history" class="nav-item">Historique</router-link>
      <router-link to="/profile" class="nav-item">Profil</router-link>
      <router-link to="/exit" class="nav-item exit">Exit</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavigationBar",
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.logo-img {
  height: 4rem;
  width: auto;
}

.nav-menu {
  display: flex;
  gap: 2rem;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-item.exit {
  background-color: #e74c3c;
}

.nav-item.exit:hover {
  background-color: #c0392b;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }
}
</style>
