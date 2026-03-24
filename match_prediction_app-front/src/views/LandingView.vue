<template>
  <div
    class="landing-container"
    @mousemove="onMouseMove"
    ref="container"
  >
    <!-- Animated Particle Field -->
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>

    <!-- Liquid Glass Background Blobs -->
    <div class="glass-blob blob-1"></div>
    <div class="glass-blob blob-2"></div>
    <div class="glass-blob blob-3"></div>
    <div class="glass-blob blob-4"></div>

    <!-- Mouse Glow Follower -->
    <div
      class="mouse-glow"
      :style="{
        left: mouseX + 'px',
        top: mouseY + 'px'
      }"
    ></div>

    <!-- Navigation -->
    <nav class="glass-nav" :class="{ scrolled: isScrolled }">
      <div class="nav-inner">
        <div class="nav-brand">
          <img src="@/assets/logo.png" alt="Logo" class="nav-logo" />
          <span class="nav-title">MatchPredict</span>
        </div>
        <div class="nav-links" :class="{ open: menuOpen }">
          <a href="#features" @click="menuOpen = false">Fonctionnalités</a>
          <a href="#stats" @click="menuOpen = false">Statistiques</a>
          <a href="#testimonials" @click="menuOpen = false">Avis</a>
          <router-link to="/login" class="nav-btn-ghost">
            Connexion
          </router-link>
          <router-link to="/register" class="nav-btn-solid">
            S'inscrire
          </router-link>
        </div>
        <button class="hamburger" @click="menuOpen = !menuOpen">
          <span :class="{ active: menuOpen }"></span>
          <span :class="{ active: menuOpen }"></span>
          <span :class="{ active: menuOpen }"></span>
        </button>
      </div>
    </nav>

    <main class="content">
      <!-- HERO -->
      <section class="hero-section">
        <div class="hero-badge" v-observe-visibility="onBadgeVisible">
          <span class="badge-dot"></span>
          Nouveau — Prédictions Euro 2026 disponibles
        </div>

        <h1 class="hero-title" ref="heroTitle">
          <span class="line">Prédisez chaque</span>
          <span class="line gradient-text">match avec l'IA</span>
        </h1>

        <p class="hero-subtitle">
          Des algorithmes entraînés sur <strong>20 ans</strong> de données
          sportives. Précision inégalée. Design immersif.
        </p>

        <!-- Futuristic Orb -->
        <div class="orb-wrapper">
          <div class="orb-ring ring-1"></div>
          <div class="orb-ring ring-2"></div>
          <div class="orb-ring ring-3"></div>
          <div class="orb-core">
            <div class="orb-inner-glow"></div>
            <div class="orb-surface">
              <svg viewBox="0 0 100 100" class="orb-svg">
                <circle
                  cx="50" cy="50" r="40"
                  fill="none"
                  stroke="rgba(255,255,255,0.1)"
                  stroke-width="0.5"
                  stroke-dasharray="4 4"
                >
                  <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="0 50 50"
                    to="360 50 50"
                    dur="20s"
                    repeatCount="indefinite"
                  />
                </circle>
                <circle
                  cx="50" cy="50" r="30"
                  fill="none"
                  stroke="rgba(255,255,255,0.08)"
                  stroke-width="0.5"
                  stroke-dasharray="2 6"
                >
                  <animateTransform
                    attributeName="transform"
                    type="rotate"
                    from="360 50 50"
                    to="0 50 50"
                    dur="15s"
                    repeatCount="indefinite"
                  />
                </circle>
              </svg>
            </div>
            <span class="orb-icon">⚽</span>
          </div>
        </div>

        <div class="cta-group">
          <router-link to="/register" class="btn btn-primary">
            <span>Commencer gratuitement</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </router-link>
          <button class="btn btn-glass" @click="playDemo">
            <span class="play-icon">▶</span>
            Voir la démo
          </button>
        </div>

        <!-- Trust Logos -->
        <div class="trust-bar">
          <span class="trust-label">Ils nous font confiance</span>
          <div class="trust-logos">
            <div class="trust-logo">ESPN</div>
            <div class="trust-logo">L'Équipe</div>
            <div class="trust-logo">Sky Sports</div>
            <div class="trust-logo">beIN</div>
            <div class="trust-logo">RMC Sport</div>
          </div>
        </div>
      </section>

      <!-- STATS COUNTER -->
      <section id="stats" class="stats-section">
        <div class="stats-grid">
          <div
            v-for="(stat, i) in stats"
            :key="i"
            class="glass-card stat-card"
          >
            <span class="stat-number">
              {{ animatedStats[i] }}{{ stat.suffix }}
            </span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </section>

      <!-- FEATURES -->
      <section id="features" class="features-section">
        <div class="section-header">
          <span class="section-tag">Fonctionnalités</span>
          <h2 class="section-title">
            Tout ce qu'il faut pour <span class="gradient-text">gagner</span>
          </h2>
          <p class="section-desc">
            Des outils de pointe alimentés par l'intelligence artificielle.
          </p>
        </div>

        <div class="features-grid">
          <div
            v-for="(feature, i) in features"
            :key="i"
            class="glass-card feature-card"
            :style="{ '--delay': i * 0.1 + 's' }"
            @mouseenter="activeFeature = i"
            @mouseleave="activeFeature = -1"
          >
            <div
              class="feature-icon-wrap"
              :style="{ background: feature.gradient }"
            >
              <span class="feature-icon">{{ feature.icon }}</span>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
            <div class="feature-arrow">→</div>
          </div>
        </div>
      </section>

      <!-- HOW IT WORKS -->
      <section class="how-section">
        <div class="section-header">
          <span class="section-tag">Comment ça marche</span>
          <h2 class="section-title">
            En <span class="gradient-text">3 étapes</span> simples
          </h2>
        </div>

        <div class="steps-track">
          <div class="steps-line"></div>
          <div
            v-for="(step, i) in steps"
            :key="i"
            class="step-item"
          >
            <div class="step-number">{{ i + 1 }}</div>
            <div class="glass-card step-card">
              <span class="step-icon">{{ step.icon }}</span>
              <h4>{{ step.title }}</h4>
              <p>{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- TESTIMONIALS -->
      <section id="testimonials" class="testimonials-section">
        <div class="section-header">
          <span class="section-tag">Avis</span>
          <h2 class="section-title">
            Ce qu'en disent <span class="gradient-text">nos utilisateurs</span>
          </h2>
        </div>

        <div class="testimonials-carousel">
          <div
            v-for="(t, i) in testimonials"
            :key="i"
            class="glass-card testimonial-card"
          >
            <div class="stars">
              <span v-for="s in 5" :key="s">★</span>
            </div>
            <p class="quote">"{{ t.quote }}"</p>
            <div class="testimonial-author">
              <div
                class="author-avatar"
                :style="{ background: t.color }"
              >
                {{ t.initials }}
              </div>
              <div>
                <strong>{{ t.name }}</strong>
                <span>{{ t.role }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FINAL CTA -->
      <section class="final-cta">
        <div class="glass-card cta-card">
          <h2>Prêt à prédire l'avenir du sport ?</h2>
          <p>
            Rejoignez des milliers d'utilisateurs et obtenez
            vos premières prédictions gratuitement.
          </p>
          <div class="cta-group">
            <router-link to="/register" class="btn btn-primary btn-lg">
              <span>Créer mon compte</span>
              <svg width="20" height="20" viewBox="0 0 24 24"
                   fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </router-link>
          </div>
          <p class="cta-note">
            Aucune carte de crédit requise • Annulation à tout moment
          </p>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer-grid">
        <div class="footer-brand">
          <img src="@/assets/logo.png" alt="Logo" class="footer-logo" />
          <p>L'IA au service de la prédiction sportive.</p>
          <div class="social-links">
            <a href="#">𝕏</a>
            <a href="#">in</a>
            <a href="#">yt</a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Produit</h4>
          <a href="#">Fonctionnalités</a>
          <a href="#">Tarifs</a>
          <a href="#">API</a>
        </div>
        <div class="footer-col">
          <h4>Entreprise</h4>
          <a href="#">À propos</a>
          <a href="#">Blog</a>
          <a href="#">Carrières</a>
        </div>
        <div class="footer-col">
          <h4>Légal</h4>
          <a href="#">CGU</a>
          <a href="#">Confidentialité</a>
          <a href="#">Cookies</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 MatchPredict. Tous droits réservés.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingView',

  data() {
    return {
      mouseX: -100,
      mouseY: -100,
      isScrolled: false,
      menuOpen: false,
      activeFeature: -1,

      stats: [
        { value: 94, suffix: '%', label: 'Précision moyenne' },
        { value: 150, suffix: 'K+', label: 'Prédictions réalisées' },
        { value: 12, suffix: 'K+', label: 'Utilisateurs actifs' },
        { value: 50, suffix: '+', label: 'Ligues couvertes' }
      ],
      animatedStats: [0, 0, 0, 0],

      features: [
        {
          icon: '🧠',
          title: 'IA Prédictive',
          desc: 'Modèles de deep learning entraînés sur 20 ans de données historiques.',
          gradient: 'linear-gradient(135deg, #667eea33, #764ba233)'
        },
        {
          icon: '⚡',
          title: 'Temps Réel',
          desc: 'Mises à jour en direct pendant les matchs avec ajustement des probabilités.',
          gradient: 'linear-gradient(135deg, #f093fb33, #f5576c33)'
        },
        {
          icon: '📊',
          title: 'Analyses Avancées',
          desc: 'Dashboards interactifs avec visualisations détaillées des statistiques.',
          gradient: 'linear-gradient(135deg, #4facfe33, #00f2fe33)'
        },
        {
          icon: '🏆',
          title: 'Multi-Sports',
          desc: 'Football, basketball, tennis, rugby et bien plus encore.',
          gradient: 'linear-gradient(135deg, #43e97b33, #38f9d733)'
        },
        {
          icon: '🔔',
          title: 'Alertes Intelligentes',
          desc: 'Notifications personnalisées pour les matchs à forte probabilité.',
          gradient: 'linear-gradient(135deg, #fa709a33, #fee14033)'
        },
        {
          icon: '🔒',
          title: 'Sécurité Maximale',
          desc: 'Chiffrement de bout en bout et respect total de vos données.',
          gradient: 'linear-gradient(135deg, #a18cd133, #fbc2eb33)'
        }
      ],

      steps: [
        {
          icon: '📱',
          title: 'Créez votre compte',
          desc: 'Inscription en 30 secondes, c\'est gratuit.'
        },
        {
          icon: '🎯',
          title: 'Choisissez vos matchs',
          desc: 'Sélectionnez les compétitions qui vous intéressent.'
        },
        {
          icon: '🏅',
          title: 'Recevez vos prédictions',
          desc: 'L\'IA analyse et vous fournit des prédictions détaillées.'
        }
      ],

      testimonials: [
        {
          quote: 'La précision est bluffante. J\'ai découvert des patterns que je n\'aurais jamais vus seul au toilette.',
          name: 'Ethan P.',
          role: 'Analyste sportif',
          initials: 'EP',
          color: 'linear-gradient(135deg, #667eea, #764ba2)'
        },
        {
          quote: 'L\'interface est magnifique et les prédictions sont étonnamment justes.',
          name: 'Sarah A.',
          role: 'Journaliste sportive',
          initials: 'SA',
          color: 'linear-gradient(135deg, #f093fb, #f5576c)'
        },
        {
          quote: 'Un outil indispensable pour tout passionné de sport. Le meilleur sur le marché.',
          name: 'Baptiste R.',
          role: 'Coach professionnel',
          initials: 'BR',
          color: 'linear-gradient(135deg, #4facfe, #00f2fe)'
        }
      ],

      particleCtx: null,
      particles: [],
      animFrame: null,
      statsAnimated: false
    }
  },

  mounted() {
    window.addEventListener('scroll', this.handleScroll)
    this.initParticles()
    this.animateParticles()
    this.observeStats()

    // Trigger hero animations
    this.$nextTick(() => {
      document.querySelector('.hero-section')?.classList.add('visible')
    })
  },

  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
    cancelAnimationFrame(this.animFrame)
  },

  methods: {
    onMouseMove(e) {
      this.mouseX = e.clientX
      this.mouseY = e.clientY + window.scrollY
    },

    handleScroll() {
      this.isScrolled = window.scrollY > 50

      // Reveal on scroll
      document.querySelectorAll('.glass-card, .step-item').forEach(el => {
        const rect = el.getBoundingClientRect()
        if (rect.top < window.innerHeight * 0.85) {
          el.classList.add('revealed')
        }
      })
    },

    // Particle system
    initParticles() {
      const canvas = this.$refs.particleCanvas
      if (!canvas) return
      canvas.width = window.innerWidth
      canvas.height = document.body.scrollHeight
      this.particleCtx = canvas.getContext('2d')

      for (let i = 0; i < 60; i++) {
        this.particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          r: Math.random() * 2 + 0.5,
          o: Math.random() * 0.5 + 0.1
        })
      }
    },

    animateParticles() {
      const ctx = this.particleCtx
      const canvas = this.$refs.particleCanvas
      if (!ctx || !canvas) return

      ctx.clearRect(0, 0, canvas.width, canvas.height)

      this.particles.forEach(p => {
        p.x += p.vx
        p.y += p.vy

        if (p.x < 0) p.x = canvas.width
        if (p.x > canvas.width) p.x = 0
        if (p.y < 0) p.y = canvas.height
        if (p.y > canvas.height) p.y = 0

        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(102, 126, 234, ${p.o})`
        ctx.fill()
      })

      // Draw connections
      for (let i = 0; i < this.particles.length; i++) {
        for (let j = i + 1; j < this.particles.length; j++) {
          const dx = this.particles[i].x - this.particles[j].x
          const dy = this.particles[i].y - this.particles[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < 120) {
            ctx.beginPath()
            ctx.moveTo(this.particles[i].x, this.particles[i].y)
            ctx.lineTo(this.particles[j].x, this.particles[j].y)
            ctx.strokeStyle = `rgba(102, 126, 234, ${0.06 * (1 - dist / 120)})`
            ctx.lineWidth = 0.5
            ctx.stroke()
          }
        }
      }

      this.animFrame = requestAnimationFrame(this.animateParticles)
    },

    // Stats counter animation
    observeStats() {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !this.statsAnimated) {
            this.statsAnimated = true
            this.countUpStats()
          }
        })
      }, { threshold: 0.3 })

      const section = document.getElementById('stats')
      if (section) observer.observe(section)
    },

    countUpStats() {
      this.stats.forEach((stat, i) => {
        let current = 0
        const step = Math.ceil(stat.value / 60)
        const interval = setInterval(() => {
          current += step
          if (current >= stat.value) {
            current = stat.value
            clearInterval(interval)
          }
          this.animatedStats[i] = current
          this.$forceUpdate()
        }, 30)
      })
    },

    playDemo() {
      alert('Démo vidéo bientôt disponible !')
    },

    onBadgeVisible() { /* placeholder */ }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ============================================
   RESET & BASE
   ============================================ */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.landing-container {
  min-height: 100vh;
  background: #06080f;
  color: #e2e8f0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* ============================================
   PARTICLE CANVAS
   ============================================ */
.particle-canvas {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

/* ============================================
   MOUSE GLOW
   ============================================ */
.mouse-glow {
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(102, 126, 234, 0.08) 0%,
    transparent 70%
  );
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
  transition: left 0.3s ease, top 0.3s ease;
}

/* ============================================
   BLOBS
   ============================================ */
.glass-blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  z-index: 0;
  opacity: 0.4;
  animation: float 25s infinite alternate ease-in-out;
}
.blob-1 {
  width: 500px;
  height: 500px;
  background: #667eea;
  top: -200px;
  left: -150px;
}
.blob-2 {
  width: 400px;
  height: 400px;
  background: #764ba2;
  bottom: 20%;
  right: -100px;
  animation-delay: -7s;
}
.blob-3 {
  width: 350px;
  height: 350px;
  background: #4facfe;
  top: 40%;
  left: 50%;
  animation-delay: -14s;
  opacity: 0.2;
}
.blob-4 {
  width: 300px;
  height: 300px;
  background: #f093fb;
  bottom: 10%;
  left: 10%;
  animation-delay: -20s;
  opacity: 0.15;
}

@keyframes float {
  0% { transform: translate(0, 0) scale(1) rotate(0deg); }
  33% { transform: translate(30px, -50px) scale(1.1) rotate(120deg); }
  66% { transform: translate(-20px, 30px) scale(0.95) rotate(240deg); }
  100% { transform: translate(50px, 80px) scale(1.15) rotate(360deg); }
}

/* ============================================
   NAVIGATION
   ============================================ */
.glass-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 1rem 2rem;
  transition: all 0.4s ease;
}
.glass-nav.scrolled {
  background: rgba(6, 8, 15, 0.8);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 0.7rem 2rem;
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  z-index: 101;
}
.nav-logo {
  height: 36px;
  filter: drop-shadow(0 0 8px rgba(102, 126, 234, 0.4));
}
.nav-title {
  font-weight: 700;
  font-size: 1.2rem;
  background: linear-gradient(135deg, #667eea, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}
.nav-links a {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s;
}
.nav-links a:hover {
  color: white;
}
.nav-btn-ghost {
  padding: 0.5rem 1.2rem !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 12px !important;
  transition: all 0.3s !important;
}
.nav-btn-ghost:hover {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}
.nav-btn-solid {
  padding: 0.5rem 1.2rem !important;
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  border-radius: 12px !important;
  color: white !important;
  font-weight: 600 !important;
  transition: all 0.3s !important;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}
.nav-btn-solid:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 101;
  padding: 4px;
}
.hamburger span {
  display: block;
  width: 24px;
  height: 2px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s;
}
.hamburger span.active:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}
.hamburger span.active:nth-child(2) {
  opacity: 0;
}
.hamburger span.active:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

/* ============================================
   CONTENT
   ============================================ */
.content {
  position: relative;
  z-index: 2;
  flex: 1;
}

/* ============================================
   HERO
   ============================================ */
.hero-section {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 8rem 2rem 4rem;
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s cubic-bezier(0.22, 1, 0.36, 1);
}
.hero-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.2rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 100px;
  font-size: 0.85rem;
  color: #a78bfa;
  margin-bottom: 2rem;
  animation: pulse-badge 3s infinite;
}
.badge-dot {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: dot-pulse 2s infinite;
}

@keyframes dot-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

@keyframes pulse-badge {
  0%, 100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.2); }
  50% { box-shadow: 0 0 0 8px rgba(102, 126, 234, 0); }
}

.hero-title {
  font-size: clamp(2.5rem, 7vw, 5rem);
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -2px;
}
.hero-title .line {
  display: block;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #667eea);
  background-size: 300% 300%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient-shift 6s ease infinite;
}

@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.hero-subtitle {
  font-size: 1.15rem;
  color: #64748b;
  max-width: 550px;
  line-height: 1.7;
  margin-bottom: 2.5rem;
  font-weight: 400;
}
.hero-subtitle strong {
  color: #a78bfa;
  font-weight: 600;
}

/* ============================================
   ORB
   ============================================ */
.orb-wrapper {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 2rem auto 3rem;
}

.orb-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1px solid rgba(102, 126, 234, 0.15);
}
.ring-1 {
  animation: spin 12s linear infinite;
  inset: -20px;
  border-style: dashed;
  border-color: rgba(102, 126, 234, 0.1);
}
.ring-2 {
  animation: spin 20s linear infinite reverse;
  inset: -40px;
  border-style: dotted;
  border-color: rgba(118, 75, 162, 0.1);
}
.ring-3 {
  animation: spin 30s linear infinite;
  inset: -60px;
  border-color: rgba(240, 147, 251, 0.06);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.orb-core {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(
    circle at 35% 35%,
    rgba(102, 126, 234, 0.4) 0%,
    rgba(118, 75, 162, 0.3) 40%,
    rgba(6, 8, 15, 0.8) 100%
  );
  box-shadow:
    0 0 60px rgba(102, 126, 234, 0.3),
    0 0 120px rgba(118, 75, 162, 0.15),
    inset 0 0 30px rgba(255, 255, 255, 0.05);
  animation: orb-hover 5s ease-in-out infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.orb-inner-glow {
  position: absolute;
  width: 60%;
  height: 60%;
  top: 15%;
  left: 15%;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.15) 0%,
    transparent 70%
  );
  filter: blur(8px);
}
.orb-surface {
  position: absolute;
  inset: 0;
}
.orb-svg {
  width: 100%;
  height: 100%;
}
.orb-icon {
  font-size: 3rem;
  z-index: 2;
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.3));
}

@keyframes orb-hover {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-15px) scale(1.03); }
}

/* ============================================
   BUTTONS
   ============================================ */
.cta-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-family: inherit;
}
.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
}
.btn-primary::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.2) 0%,
    transparent 50%
  );
  opacity: 0;
  transition: opacity 0.3s;
}
.btn-primary:hover::before {
  opacity: 1;
}
.btn-primary:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
}
.btn-primary:active {
  transform: translateY(0) scale(0.98);
}
.btn-lg {
  padding: 1.2rem 2.5rem;
  font-size: 1.1rem;
}

.btn-glass {
  background: rgba(255, 255, 255, 0.04);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
.btn-glass:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-3px);
  border-color: rgba(255, 255, 255, 0.2);
}

.play-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 50%;
  font-size: 0.7rem;
}

/* ============================================
   TRUST BAR
   ============================================ */
.trust-bar {
  margin-top: 4rem;
  text-align: center;
}
.trust-label {
  font-size: 0.8rem;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
  display: block;
  margin-bottom: 1.5rem;
}
.trust-logos {
  display: flex;
  gap: 3rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}
.trust-logo {
  font-size: 1.2rem;
  font-weight: 700;
  color: #334155;
  letter-spacing: 2px;
  text-transform: uppercase;
  transition: color 0.3s;
}
.trust-logo:hover {
  color: #667eea;
}

/* ============================================
   GLASS CARD (Global)
   ============================================ */
.glass-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px) saturate(150%);
  -webkit-backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 24px;
  box-shadow:
    0 4px 30px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.7s cubic-bezier(0.22, 1, 0.36, 1);
  transition-delay: var(--delay, 0s);
}
.glass-card.revealed {
  opacity: 1;
  transform: translateY(0);
}

/* ============================================
   STATS
   ============================================ */
.stats-section {
  padding: 4rem 2rem;
  max-width: 1100px;
  margin: 0 auto;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}
.stat-card {
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s, background 0.3s;
}
.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.04);
}
.stat-number {
  display: block;
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}
.stat-label {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

/* ============================================
   SECTION HEADERS
   ============================================ */
.section-header {
  text-align: center;
  margin-bottom: 4rem;
}
.section-tag {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.15);
  border-radius: 100px;
  font-size: 0.8rem;
  color: #a78bfa;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 1rem;
}
.section-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 1rem;
  color: white;
}
.section-desc {
  font-size: 1.1rem;
  color: #64748b;
  max-width: 500px;
  margin: 0 auto;
}

/* ============================================
   FEATURES
   ============================================ */
.features-section {
  padding: 6rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.feature-card {
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
  cursor: default;
}
.feature-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(102, 126, 234, 0.08) 0%,
    transparent 60%
  );
  opacity: 0;
  transition: opacity 0.5s;
}
.feature-card:hover::after {
  opacity: 1;
}
.feature-card:hover {
  background: rgba(255, 255, 255, 0.04);
  transform: translateY(-8px);
  border-color: rgba(102, 126, 234, 0.2);
}

.feature-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}
.feature-icon {
  font-size: 1.5rem;
}
.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: white;
}
.feature-card p {
  color: #64748b;
  line-height: 1.7;
  font-size: 0.95rem;
}
.feature-arrow {
  margin-top: 1.5rem;
  color: #667eea;
  font-size: 1.2rem;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s;
}
.feature-card:hover .feature-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* ============================================
   HOW IT WORKS
   ============================================ */
.how-section {
  padding: 6rem 2rem;
  max-width: 900px;
  margin: 0 auto;
}
.steps-track {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.steps-line {
  position: absolute;
  left: 28px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(
    180deg,
    rgba(102, 126, 234, 0.3),
    rgba(118, 75, 162, 0.3),
    rgba(240, 147, 251, 0.1)
  );
}
.step-item {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  opacity: 0;
  transform: translateX(-30px);
  transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}
.step-item.revealed {
  opacity: 1;
  transform: translateX(0);
}
.step-number {
  width: 56px;
  height: 56px;
  min-width: 56px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.2rem;
  z-index: 2;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}
.step-card {
  padding: 2rem;
  flex: 1;
}
.step-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 1rem;
}
.step-card h4 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: white;
}
.step-card p {
  color: #64748b;
  line-height: 1.6;
}

/* ============================================
   TESTIMONIALS
   ============================================ */
.testimonials-section {
  padding: 6rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
.testimonials-carousel {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.testimonial-card {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
}
.testimonial-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.04);
}
.stars {
  margin-bottom: 1.5rem;
  color: #fbbf24;
  font-size: 1rem;
  letter-spacing: 2px;
}
.quote {
  flex: 1;
  color: #cbd5e1;
  line-height: 1.7;
  font-size: 0.95rem;
  font-style: italic;
  margin-bottom: 1.5rem;
}
.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.author-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
  color: white;
}
.testimonial-author strong {
  display: block;
  font-size: 0.9rem;
  color: white;
}
.testimonial-author span {
  font-size: 0.8rem;
  color: #64748b;
}

/* ============================================
   FINAL CTA
   ============================================ */
.final-cta {
  padding: 6rem 2rem;
  max-width: 800px;
  margin: 0 auto;
}
.cta-card {
  padding: 4rem;
  text-align: center;
  background: rgba(102, 126, 234, 0.05);
  border-color: rgba(102, 126, 234, 0.15);
}
.cta-card h2 {
  font-size: clamp(1.8rem, 3vw, 2.5rem);
  font-weight: 800;
  margin-bottom: 1rem;
  color: white;
}
.cta-card > p {
  color: #64748b;
  margin-bottom: 2rem;
  font-size: 1.05rem;
  line-height: 1.7;
}
.cta-note {
  margin-top: 1.5rem;
  font-size: 0.8rem;
  color: #475569;
}

/* ============================================
   FOOTER
   ============================================ */
.footer {
  position: relative;
  z-index: 2;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding: 4rem 2rem 2rem;
}
.footer-grid {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
}
.footer-brand p {
  color: #475569;
  margin-top: 0.75rem;
  line-height: 1.6;
  font-size: 0.9rem;
}
.footer-logo {
  height: 32px;
  opacity: 0.7;
}
.social-links {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
}
.social-links a {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 700;
  transition: all 0.3s;
}
.social-links a:hover {
  background: rgba(102, 126, 234, 0.2);
  color: white;
  border-color: rgba(102, 126, 234, 0.3);
}
.footer-col h4 {
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.footer-col a {
  display: block;
  color: #475569;
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  transition: color 0.3s;
}
.footer-col a:hover {
  color: #a78bfa;
}
.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.03);
}
.footer-bottom p {
  font-size: 0.8rem;
  color: #334155;
}

/* ============================================
   RESPONSIVE
   ============================================ */
@media (max-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .testimonials-carousel {
    grid-template-columns: repeat(2, 1fr);
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .nav-links {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(6, 8, 15, 0.95);
    backdrop-filter: blur(20px);
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    transform: translateY(-100%);
    transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
    z-index: 100;
  }
  .nav-links.open {
    transform: translateY(0);
  }
  .nav-links a {
    font-size: 1.2rem;
  }
  .hamburger {
    display: flex;
  }

  .hero-title {
    letter-spacing: -1px;
  }
  .features-grid,
  .testimonials-carousel {
    grid-template-columns: 1fr;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .cta-card {
    padding: 2.5rem 1.5rem;
  }
  .trust-logos {
    gap: 1.5rem;
  }
  .trust-logo {
    font-size: 0.9rem;
  }
  .orb-wrapper {
    width: 150px;
    height: 150px;
  }
  .orb-icon {
    font-size: 2.2rem;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .hero-section {
    padding: 7rem 1.5rem 3rem;
  }
  .cta-group {
    flex-direction: column;
    width: 100%;
  }
  .btn {
    justify-content: center;
    width: 100%;
  }
}

/* ============================================
   SMOOTH SCROLL
   ============================================ */
html {
  scroll-behavior: smooth;
}
</style>