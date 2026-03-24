<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <section class="cta">
    <div class="cta-container">
      <div class="cta-card">
        <h2>Prêt à changer votre façon de <span>parier</span> ?</h2>
        <p>Rejoignez des milliers de passionnés qui utilisent déjà Match-Prediction pour optimiser leurs analyses sportives.</p>
        <div class="cta-actions">
          <RouterLink to="/register" class="primary-btn">Créer un compte gratuitement</RouterLink>
          <RouterLink to="/login" class="secondary-btn">Se connecter</RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta {
  padding: 100px 2rem;
}

.cta-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cta-card {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border: 1px solid rgba(102, 126, 234, 0.2);
  padding: 6rem 4rem;
  border-radius: 40px;
  text-align: center;
  backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
}

.cta-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

h2 {
  font-size: 3.5rem;
  color: white;
  margin-bottom: 1.5rem;
  font-weight: 800;
  line-height: 1.1;
}

h2 span {
  color: #fbbf24;
}

p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.25rem;
  max-width: 600px;
  margin: 0 auto 3rem;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.primary-btn {
  background: white;
  color: #667eea;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  background: #f8f9fa;
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  h2 {
    font-size: 2.5rem;
  }
  
  .cta-card {
    padding: 4rem 2rem;
  }
}
</style>
