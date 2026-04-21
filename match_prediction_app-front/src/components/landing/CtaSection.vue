<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterLink } from 'vue-router';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';
import SplitType from 'split-type';

gsap.registerPlugin(ScrollTrigger);

const ctaRef = ref(null);
const btnRef = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    
    // 1. Entrance animation
    const ctaTitle = new SplitType('.cta-card h2', { types: 'words, chars' });
    
    // Restore highlight to specific words that SplitType might have stripped tags from
    ctaTitle.words.forEach(word => {
      if (word.textContent.includes('parier')) {
        word.classList.add('text-highlight');
      }
    });
    
    gsap.set('.cta-card', { y: 100, opacity: 0, scale: 0.95 });
    gsap.set(ctaTitle.chars, { y: 50, opacity: 0 });
    gsap.set('.cta-card p', { y: 20, opacity: 0 });
    gsap.set('.cta-actions > *', { y: 20, opacity: 0 });

    const ctaTl = gsap.timeline({
      scrollTrigger: {
        trigger: '.cta-container',
        start: 'top 85%',
      }
    });

    ctaTl.to('.cta-card', { y: 0, opacity: 1, scale: 1, duration: 0.8, ease: 'power3.out' })
         .to(ctaTitle.chars, { y: 0, opacity: 1, stagger: 0.02, duration: 0.6, ease: 'power4.out' }, '-=0.4')
         .to('.cta-card p', { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.4')
         .to('.cta-actions > *', { y: 0, opacity: 1, stagger: 0.1, duration: 0.6, ease: 'power3.out' }, '-=0.4');

    // 2. Magnetic Button Effect
    if (btnRef.value && btnRef.value.$el) {
      const btn = btnRef.value.$el;
      
      const xTo = gsap.quickTo(btn, "x", {duration: 0.4, ease: "power3"});
      const yTo = gsap.quickTo(btn, "y", {duration: 0.4, ease: "power3"});

      btn.addEventListener("mousemove", (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        xTo(x * 0.3); // Magnetic pull strength
        yTo(y * 0.3);
      });

      btn.addEventListener("mouseleave", () => {
        xTo(0);
        yTo(0);
      });
    }

  }, ctaRef.value);
});

onUnmounted(() => {
  ctx.revert();
});
</script>

<template>
  <section class="cta" ref="ctaRef">
    <div class="cta-container">
      <div class="cta-card">
        <h2>Prêt à changer votre façon de <span>parier</span> ?</h2>
        <p>Rejoignez des milliers de passionnés qui utilisent déjà Match-Prediction pour optimiser leurs analyses sportives.</p>
        <div class="cta-actions">
          <RouterLink to="/register" class="primary-btn" ref="btnRef">Créer un compte gratuitement</RouterLink>
          <RouterLink to="/login" class="secondary-btn">Se connecter</RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta {
  padding: 100px 2rem;
}

.cta-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cta-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  padding: 6rem 4rem;
  border-radius: 40px;
  text-align: center;
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
  background-image: linear-gradient(rgba(10, 10, 26, 0.7), rgba(10, 10, 26, 0.8)), url("@/assets/ballon5.jpg");
  background-size: cover;
  background-position: center;
}

.cta-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(224, 38, 255, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

h2 {
  font-size: 3.5rem;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  font-weight: 800;
  line-height: 1.1;
}

/* Rely on global .text-highlight styles in App.vue */
h2 span {
  display: inline-block;
}

p {
  color: var(--text-secondary);
  font-size: 1.25rem;
  max-width: 600px;
  margin: 0 auto 3rem;
  line-height: 1.6;
}

.cta-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.primary-btn {
  background: var(--accent-gradient);
  color: white;
  padding: 1.2rem 3rem;
  border-radius: 50px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(224, 38, 255, 0.3);
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(224, 38, 255, 0.5);
  filter: brightness(1.1);
}

.secondary-btn {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  color: white;
  padding: 1.2rem 3rem;
  border-radius: 50px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.secondary-btn:hover {
  background: var(--glass-hover);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}


@media (max-width: 768px) {
  h2 {
    font-size: 2.5rem;
  }
  
  .cta-card {
    padding: 4rem 2rem;
  }
}

/* SplitType Masking */
:deep(.word) {
  overflow: hidden;
  padding-bottom: 0.1em;
  margin-bottom: -0.1em;
}
</style>
