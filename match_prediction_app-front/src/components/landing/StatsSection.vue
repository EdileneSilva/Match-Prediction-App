<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { STATS } from './constants';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const statsRef = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    
    // 1. Cards Parallax / Fade in
    gsap.set('.stat-card', { y: 50, opacity: 0 });
    gsap.to('.stat-card', {
      y: 0,
      opacity: 1,
      stagger: 0.1,
      duration: 0.8,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: '.stats-container',
        start: 'top 85%',
      }
    });

    // 2. Animated Counters
    gsap.utils.toArray('.stat-num').forEach((el) => {
      const target = parseFloat(el.getAttribute('data-target'));
      gsap.to(el, {
        innerHTML: target,
        duration: 2,
        snap: { innerHTML: 1 },
        ease: 'power3.out',
        scrollTrigger: {
          trigger: '.stats-container',
          start: 'top 85%',
        }
      });
    });

  }, statsRef.value);
});

onUnmounted(() => {
  ctx.revert();
});
</script>

<template>
  <section class="stats" ref="statsRef">
    <div class="stats-bg"></div>
    <div class="stats-container">
      <div v-for="(stat, index) in STATS" :key="index" class="stat-card">
        <div class="stat-value">
          <span class="stat-num" :data-target="stat.value">0</span><span>{{ stat.suffix }}</span>
        </div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.stats {
  padding: 80px 2rem;
  position: relative;
  overflow: hidden;
  border-top: 1px solid var(--glass-border);
  border-bottom: 1px solid var(--glass-border);
}

.stats-bg {
  position: absolute;
  top: -50%;
  left: 0;
  width: 100%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(0, 212, 255, 0.05) 0%, rgba(0, 0, 0, 0) 70%);
  z-index: 0;
  pointer-events: none;
}

.stats-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  position: relative;
  z-index: 1;
}

.stat-card {
  text-align: center;
  padding: 2.5rem;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
}

.stat-value {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: baseline;
}

.stat-value span:last-child {
  font-size: 1.5rem;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-left: 2px;
  font-weight: 700;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
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
