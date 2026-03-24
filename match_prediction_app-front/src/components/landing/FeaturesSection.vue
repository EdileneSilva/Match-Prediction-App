<script setup>
import { FEATURES } from './constants';
</script>

<template>
  <section id="features" class="features">
    <div class="features-container">
      <div class="section-header">
        <div class="section-badge">Fonctionnalités</div>
        <h2>Une technologie de pointe pour des <span>résultats réels</span></h2>
        <p>Notre plateforme combine expertise sportive et algorithmes de pointe.</p>
      </div>

      <div class="features-grid">
        <div v-for="(feature, index) in FEATURES" :key="index" class="feature-card">
          <div class="icon-box" :style="{ background: feature.gradient }">
            <img v-if="feature.icon.includes('/')" :src="feature.icon" :alt="feature.title" class="feature-icon-img" />
            <span v-else class="feature-icon">{{ feature.icon }}</span>
          </div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.features {
  padding: 100px 2rem;
  position: relative;
}

.features-container {
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

h2 span {
  color: #fbbf24;
}

.section-header p {
  font-size: 1.15rem;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 3rem 2rem;
  border-radius: 30px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(102, 126, 234, 0.3);
}

.icon-box {
  width: 70px;
  height: 70px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
}

.feature-icon {
  font-size: 2rem;
}

.feature-icon-img {
  width: 40px;
  height: 40px;
  object-fit: contain;
  filter: brightness(0) invert(1); /* Makes the icon white if it's black */
}

h3 {
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1rem;
  font-weight: 700;
}

.feature-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

@media (max-width: 768px) {
  h2 {
    font-size: 2.2rem;
  }
}
</style>
