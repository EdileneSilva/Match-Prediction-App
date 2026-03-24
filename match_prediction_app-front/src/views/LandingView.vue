<script setup>
import { onMounted } from 'vue';
import NavBar from '@/components/landing/NavBar.vue';
import HeroSection from '@/components/landing/HeroSection.vue';
import StatsSection from '@/components/landing/StatsSection.vue';
import FeaturesSection from '@/components/landing/FeaturesSection.vue';
import StepsSection from '@/components/landing/StepsSection.vue';
import TestimonialsSection from '@/components/landing/TestimonialsSection.vue';
import CtaSection from '@/components/landing/CtaSection.vue';
import FooterSection from '@/components/landing/FooterSection.vue';

onMounted(() => {
  window.scrollTo(0, 0);
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
/* Global styles for the landing page to ensure consistency */
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.1);
}

.landing-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  overflow-x: hidden;
}

/* Base styles for buttons used across sections if not scoped */
.primary-btn {
  cursor: pointer;
}

.secondary-btn {
  cursor: pointer;
}
</style>