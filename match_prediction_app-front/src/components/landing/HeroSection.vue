<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <section class="hero">
    <div class="hero-container">
      <div class="hero-content">
        <div class="badge">Predictly v2.0 est arrivé</div>
        <h1>L'Intelligence Artificielle au service de vos <span>Victoires</span></h1>
        <p>Les prédictions de football les plus précises grâce à nos modèles d'IA avancés et l'analyse de données en temps réel.</p>
        <div class="hero-actions">
          <RouterLink to="/register" class="primary-btn">Démarrez maintenant</RouterLink>
          <a href="#features" class="secondary-btn">En savoir plus</a>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 100px 2rem 60px;
  position: relative;
  overflow: hidden;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.hero-content {
  max-width: 700px;
  position: relative;
  z-index: 2;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 50px;
  color: #a3bffa;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

h1 {
  font-size: 4rem;
  line-height: 1.1;
  font-weight: 800;
  color: white;
  margin-bottom: 1.5rem;
}

h1 span {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

p {
  font-size: 1.25rem;
  color: #a0aec0;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  h1 {
    font-size: 2.8rem;
  }
  
  .hero-content {
    text-align: center;
  }
  
  .hero-actions {
    justify-content: center;
  }
}
</style>
