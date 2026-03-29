<script setup>
import { TESTIMONIALS } from './constants';
</script>

<template>
  <section class="testimonials">
    <div class="testimonials-container">
      <div class="section-header">
        <div class="section-badge">Témoignages</div>
        <h2>Ils nous font <span>confiance</span></h2>
        <p>Découvrez les retours de nos utilisateurs de la version bêta.</p>
      </div>

      <div class="testimonials-grid">
        <div v-for="(item, index) in TESTIMONIALS" :key="index" class="testimonial-card">
          <div class="quote-icon">"</div>
          <p class="quote-text">{{ item.quote }}</p>
          <div class="testimonial-footer">
            <div class="user-avatar" :style="{ background: item.color }">{{ item.initials }}</div>
            <div class="user-info">
              <div class="user-name">{{ item.name }}</div>
              <div class="user-role">{{ item.role }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.testimonials {
  padding: 100px 2rem;
}

.testimonials-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 5rem;
}

.section-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 50px;
  color: #a3bffa;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 3rem;
  color: white;
  margin-bottom: 1.5rem;
  font-weight: 800;
}

/* Rely on global styles in App.vue */
h2 span {
  display: inline-block;
}

/* Base adjustment for words if needed */
:deep(.word) {
  display: inline-block;
  vertical-align: top;
}


.section-header p {
  color: rgba(255, 255, 255, 0.85);
  font-size: 1.15rem;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.testimonial-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  padding: 3rem 2rem;
  border-radius: 30px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: all 0.3s ease;
  position: relative;
}

.testimonial-card:hover {
  background: var(--glass-hover);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
}


.quote-icon {
  font-size: 5rem;
  color: var(--accent-secondary);

  font-family: serif;
  line-height: 1;
  position: absolute;
  top: 1rem;
  right: 2rem;
  opacity: 0.1;
}

.quote-text {
  color: white;
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  font-style: italic;
}

.testimonial-footer {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {

  width: 50px;
  height: 50px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
}

.user-name {
  color: white;
  font-weight: 600;
  font-size: 1rem;
}

.user-role {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  h2 {
    font-size: 2.2rem;
  }
}
</style>
