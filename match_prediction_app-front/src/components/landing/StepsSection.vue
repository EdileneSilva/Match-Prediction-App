<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { STEPS } from './constants';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';
import SplitType from 'split-type';

gsap.registerPlugin(ScrollTrigger);

const stepsRef = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    
    // 1. Header Animation
    const headerTitle = new SplitType('.section-header h2', { types: 'words, chars' });
    
    gsap.set('.section-badge', { y: 20, opacity: 0 });
    gsap.set(headerTitle.chars, { y: 50, opacity: 0 });
    gsap.set('.section-header p', { y: 20, opacity: 0 });

    const headerTl = gsap.timeline({
      scrollTrigger: {
        trigger: '.section-header',
        start: 'top 80%',
      }
    });

    headerTl.to('.section-badge', { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' })
            .to(headerTitle.chars, { y: 0, opacity: 1, stagger: 0.015, duration: 0.6, ease: 'power4.out' }, '-=0.4')
            .to('.section-header p', { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.4');

    // 2. Steps and Connectors Animation
    gsap.set('.step-item', { y: 50, opacity: 0 });
    gsap.set('.step-connector', { scaleX: 0, transformOrigin: 'left center' });

    const stepsTl = gsap.timeline({
      scrollTrigger: {
        trigger: '.steps-grid',
        start: 'top 75%',
      }
    });

    // Stagger step items
    stepsTl.to('.step-item', {
      y: 0,
      opacity: 1,
      stagger: 0.3,
      duration: 0.8,
      ease: 'back.out(1.2)'
    });

    // Animate connectors in parallel with items
    stepsTl.to('.step-connector', {
      scaleX: 1,
      stagger: 0.3,
      duration: 0.8,
      ease: 'power3.inOut'
    }, 0.2); // start slightly after the first item starts appearing

  }, stepsRef.value);
});

onUnmounted(() => {
  ctx.revert();
});
</script>

<template>
  <section class="steps" ref="stepsRef">
    <div class="steps-container">
      <div class="section-header">
        <div class="section-badge">Processus</div>
        <h2>Comment ça <span class="highlight">marche</span> ?</h2>
        <p class="section-desc">Trois étapes simples pour transformer vos analyses sportives.</p>
      </div>

      <div class="steps-grid">
        <div v-for="(step, index) in STEPS" :key="index" class="step-item">
          <div class="step-icon-wrapper">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-icon">
              <img v-if="step.icon.includes('/')" :src="step.icon" :alt="step.title" class="step-icon-img" />
              <span v-else>{{ step.icon }}</span>
            </div>
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

h2 span.highlight {
  color: #fbbf24;
}

.section-header p {
  color: rgba(255, 255, 255, 0.85);
  font-size: 1.15rem;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6rem;
  position: relative;
}

.step-item {
  text-align: center;
  position: relative;
  z-index: 2;
}

.step-icon-wrapper {
  width: 180px;
  height: 180px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2.5rem;
  position: relative;
}

.step-number {
  position: absolute;
  top: -15px;
  right: -15px;
  width: 55px;
  height: 55px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 800;
  font-size: 1.2rem;
  box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

.step-icon {
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-icon-img {
  width: 100px;
  height: 100px;
  object-fit: contain;
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
  top: 90px;
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

/* SplitType Masking */
:deep(.word) {
  overflow: hidden;
  padding-bottom: 0.1em;
  margin-bottom: -0.1em;
}
</style>
