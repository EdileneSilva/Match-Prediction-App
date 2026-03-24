<script setup>
import { STATS } from './constants';
</script>

<template>
  <section class="stats">
    <div class="stats-container">
      <div v-for="(stat, index) in STATS" :key="index" class="stat-card">
        <div class="stat-value">
          {{ stat.value }}<span>{{ stat.suffix }}</span>
        </div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.stats {
  padding: 60px 2rem;
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.stats-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.stat-card {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.stat-value {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: baseline;
}

.stat-value span {
  font-size: 1.5rem;
  color: #667eea;
  margin-left: 2px;
}

.stat-label {
  color: #a0aec0;
  font-size: 1rem;
  font-weight: 500;
}

@media (max-width: 992px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
}
</style>
