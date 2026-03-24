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
  // Clear any potential leftover animations or canvas if needed
  // For now, we just ensure a clean state
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
  background-color: #0f172a;
  color: white;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  overflow-x: hidden;
}

/* Base styles for buttons used across sections if not scoped */
.primary-btn {
  cursor: pointer;
}

.secondary-btn {
  cursor: pointer;
}

/* Background elements for depth without heavy animations */
.landing-page::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(118, 75, 162, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}
</style>