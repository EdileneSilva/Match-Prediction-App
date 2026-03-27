<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { FEATURES } from './constants';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';
import SplitType from 'split-type';

gsap.registerPlugin(ScrollTrigger);

const featuresRef = ref(null);
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
        start: 'top 80%', // trigger when top of header is 80% down the viewport
      }
    });

    headerTl.to('.section-badge', { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' })
            .to(headerTitle.chars, { y: 0, opacity: 1, stagger: 0.015, duration: 0.6, ease: 'power4.out' }, '-=0.4')
            .to('.section-header p', { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.4');

    // 2. Cards Stagger Animation
    gsap.set('.feature-card', { y: 80, opacity: 0 });

    gsap.to('.feature-card', {
      y: 0,
      opacity: 1,
      stagger: 0.15,
      duration: 0.8,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: '.features-grid',
        start: 'top 75%',
      }
    });

  }, featuresRef.value);
});

onUnmounted(() => {
  ctx.revert();
});
</script>

<template>
  <section id="features" class="features" ref="featuresRef">
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
  width: 135px;
  height: 135px;
  border-radius: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2.5rem;
}

.feature-icon {
  font-size: 2rem;
}

.feature-icon-img {
  width: 80px;
  height: 80px;
  object-fit: contain;
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

/* SplitType Masking */
:deep(.word) {
  overflow: hidden;
  padding-bottom: 0.1em;
  margin-bottom: -0.1em;
}
</style>
