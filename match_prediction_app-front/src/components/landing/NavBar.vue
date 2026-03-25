<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-logo">
        <div class="logo-icon">
          <img src="@/assets/logo.png" alt="logo" />
        </div>
        <span>Match Prediction</span>
      </div>

      <div class="nav-links">
        <RouterLink to="/predictions" class="nav-link">Prédictions</RouterLink>
        <RouterLink to="/history" class="nav-link">Historique</RouterLink>
        <RouterLink to="/login" class="nav-link">Connexion</RouterLink>
        <RouterLink to="/register" class="nav-btn">Essai Gratuit</RouterLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1000;
  display: flex;
  align-items: center;
}

.nav-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
}

.logo-icon {
  width: 78px;
  height: 78px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  overflow: hidden;
}

.logo-icon img {
  width: 200%;
  height: 200%;
  object-fit: contain;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: #a0aec0;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: white;
}

.nav-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 0.8rem 1.8rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
  }
}
</style>