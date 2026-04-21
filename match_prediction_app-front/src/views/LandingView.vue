<script setup>
import { onMounted, nextTick } from 'vue';
import NavBar from '@/components/NavigationBar.vue';
import HeroSection from '@/components/landing/HeroSection.vue';
import StatsSection from '@/components/landing/StatsSection.vue';
import FeaturesSection from '@/components/landing/FeaturesSection.vue';
import StepsSection from '@/components/landing/StepsSection.vue';
import TestimonialsSection from '@/components/landing/TestimonialsSection.vue';
import CtaSection from '@/components/landing/CtaSection.vue';
import FooterSection from '@/components/landing/FooterSection.vue';

onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'instant' });
    }, 50);
  });
});
</script>

<template>
  <div class="landing-page">
    <NavBar />
    
    <main>
      <HeroSection />
      <StatsSection />
      <FeaturesSection />
      <StepsSection />
      <TestimonialsSection />
      <CtaSection />
    </main>

    <FooterSection />
  </div>
</template>

<style>
.landing-page {
  background: var(--bg-cosmic);
  color: var(--text-primary);
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
}

.primary-btn, .secondary-btn {
  cursor: pointer;
}

</style>