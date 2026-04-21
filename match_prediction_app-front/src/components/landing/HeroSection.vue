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
    
    // Restore highlight to specific words that SplitType might have stripped tags from
    title.words.forEach(word => {
      if (word.textContent.includes('Victoires')) {
        word.classList.add('text-highlight');
      }
    });
    
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
        <img src="@/assets/cosmic-ball.png" alt="Futuristic Soccer Ball" class="ballon-img" />
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
  padding: 180px 2rem 140px;
  position: relative;
  overflow: hidden;
  background-image: linear-gradient(to bottom, rgba(10, 10, 26, 0.7), rgba(10, 10, 26, 0.9)), url("@/assets/stadium2.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
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
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  overflow: hidden;
  
  /* Effet Cosmic sur le conteneur */
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.4), 
    0 0 20px rgba(224, 38, 255, 0.1);
    
  transition: all 0.3s ease;
  will-change: transform, clip-path;
}

.hero-image-top:hover {
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.5), 
    0 0 30px rgba(0, 212, 255, 0.2);
  border-color: rgba(0, 212, 255, 0.3);
}

.ballon-img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}

.hero-content {
  max-width: 800px;
  position: relative;
  z-index: 2;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: var(--glass-bg);
  border: 1px solid var(--accent-secondary);
  border-radius: 50px;
  color: var(--accent-secondary);
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 2rem;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
}

h1 {
  font-size: 4rem;
  line-height: 1.1;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

/* Rely on global .text-highlight styles in App.vue */
h1 span {
  display: inline-block;
}

p {
  font-size: 1.25rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.primary-btn {
  background: var(--accent-gradient);
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
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
  padding: 1rem 2.5rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.secondary-btn:hover {
  background: var(--glass-hover);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
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
