<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterLink } from 'vue-router';
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';
import SplitType from 'split-type';

gsap.registerPlugin(ScrollTrigger);

const heroRef = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    // 1. Text Reveal with SplitType (Premium Mask Reveal)
    const h1Element = heroRef.value.querySelector('h1');
    const title = new SplitType(h1Element, { types: 'lines, words' });
    
    const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });

    // Ensure lines mask the words sliding up
    gsap.set(title.lines, { overflow: 'hidden' });

    // Initial state
    gsap.set('.badge', { y: 20, opacity: 0 });
    gsap.set(title.words, { y: 100, opacity: 0 });
    gsap.set('p', { y: 20, opacity: 0 });
    gsap.set('.hero-actions .primary-btn, .hero-actions .secondary-btn', { y: 20, opacity: 0 });
    gsap.set('.hero-image-top', { clipPath: 'polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)' });
    gsap.set('.ballon-img', { scale: 1.2 });

    // Entrance Animation
    tl.to('.hero-image-top', { 
      clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)', 
      duration: 1.5,
      ease: 'power3.inOut'
    })
    .to('.ballon-img', {
      scale: 1,
      duration: 1.5,
      ease: 'power3.inOut'
    }, '<')
    .to('.badge', {
      y: 0,
      opacity: 1,
      duration: 0.8
    }, '-=0.8')
    .to(title.words, {
      y: 0,
      opacity: 1,
      stagger: 0.05,
      duration: 0.8,
      ease: 'power4.out'
    }, '-=0.6')
    .to('p', {
      y: 0,
      opacity: 1,
      duration: 0.8
    }, '-=0.6')
    .to('.hero-actions .primary-btn, .hero-actions .secondary-btn', {
      y: 0,
      opacity: 1,
      stagger: 0.1,
      duration: 0.8
    }, '-=0.6');

    // Parallax Effect on scroll (Desktop only)
    let mm = gsap.matchMedia();
    mm.add("(min-width: 768px)", () => {
      gsap.to('.hero-image-top', {
        yPercent: 15,
        ease: 'none',
        scrollTrigger: {
          trigger: heroRef.value,
          start: 'top top',
          end: 'bottom top',
          scrub: true,
        }
      });
    });

  }, heroRef.value);
});

onUnmounted(() => {
  ctx.revert(); // clean up GSAP to prevent memory leaks
});
</script>

<template>
  <section class="hero" ref="heroRef">
    <div class="hero-container">
      <div class="hero-image-top">
        <img src="@/assets/Ballon2.png" alt="Ballon" class="ballon-img" />
      </div>
      <div class="hero-content">
        <div class="badge">Match Prediction v1.0 est arrivé</div>
        <h1>L'Intelligence Artificielle au service de vos <span>Victoires</span></h1>
        <p>Les prédictions de football les plus précises grâce à nos modèles d'IA avancés et l'analyse de données en temps réel.</p>
        <div class="hero-actions">
          <RouterLink to="/register" class="primary-btn">Démarrez maintenant</RouterLink>
          <a href="#features" class="secondary-btn">En savoir plus</a>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 80px 2rem 40px;
  position: relative;
  overflow: hidden;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero-image-top {
  margin: 0 auto 2rem;
  max-width: 750px;
  width: 95%;
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.03);
  overflow: hidden;
  
  /* Effet Néomorphisme sur le conteneur */
  box-shadow: 
    20px 20px 40px rgba(0, 0, 0, 0.25), 
    -20px -20px 40px rgba(255, 255, 255, 0.05),
    inset 2px 2px 5px rgba(255, 255, 255, 0.1),
    inset -2px -2px 5px rgba(0, 0, 0, 0.1);
    
  transition: box-shadow 0.3s ease; /* Removed transform to avoid GSAP conflict */
  will-change: transform, clip-path; /* Perf optimization */
}

.hero-image-top:hover {
  /* Only animate shadow on hover to avoid conflicting with GSAP's yPercent */
  box-shadow: 
    25px 25px 50px rgba(0, 0, 0, 0.3), 
    -25px -25px 50px rgba(255, 255, 255, 0.05),
    inset 2px 2px 5px rgba(255, 255, 255, 0.1),
    inset -2px -2px 5px rgba(0, 0, 0, 0.1);
}

.ballon-img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover; /* Remplit bien le rectangle */
}

.hero-content {
  max-width: 800px;
  position: relative;
  z-index: 2;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

h1 {
  font-size: 4rem;
  line-height: 1.1;
  font-weight: 800;
  color: white;
  margin-bottom: 1.5rem;
}

h1 span {
  color: #fbbf24; /* Use a golden/yellow for "Victoires" to stand out on purple */
}

p {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
}

.secondary-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  h1 {
    font-size: 2.8rem;
  }
  
  .hero-content {
    text-align: center;
  }
  
  .hero-actions {
    justify-content: center;
  }
}

/* SplitType Masking */
:deep(.word) {
  overflow: hidden;
  padding-bottom: 0.1em;
  margin-bottom: -0.1em;
}
</style>
