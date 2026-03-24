<script setup>
import { STEPS } from './constants';
</script>

<template>
  <section class="steps">
    <div class="steps-container">
      <div class="section-header">
        <div class="section-badge">Processus</div>
        <h2>Comment ça <span>marche</span> ?</h2>
        <p>Trois étapes simples pour transformer vos analyses sportives.</p>
      </div>

      <div class="steps-grid">
        <div v-for="(step, index) in STEPS" :key="index" class="step-item">
          <div class="step-icon-wrapper">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-icon">{{ step.icon }}</div>
          </div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.desc }}</p>
          <div v-if="index < STEPS.length - 1" class="step-connector"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.steps {
  padding: 100px 2rem;
  background: rgba(0, 0, 0, 0.2);
}

.steps-container {
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
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-header p {
  color: #a0aec0;
  font-size: 1.15rem;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4rem;
  position: relative;
}

.step-item {
  text-align: center;
  position: relative;
  z-index: 2;
}

.step-icon-wrapper {
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  position: relative;
}

.step-number {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 35px;
  height: 35px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 800;
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

.step-icon {
  font-size: 2.5rem;
}

h3 {
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1rem;
  font-weight: 700;
}

.step-item p {
  color: #a0aec0;
  line-height: 1.6;
}

.step-connector {
  position: absolute;
  top: 50px;
  right: -50%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #667eea, transparent);
  opacity: 0.2;
  z-index: -1;
}

@media (max-width: 992px) {
  .steps-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  
  .step-connector {
    display: none;
  }
}
</style>
