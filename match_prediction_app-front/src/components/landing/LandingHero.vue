<template>
  <section class="hero-section" :class="{ visible: isVisible }">
    <div class="hero-badge">
      <span class="badge-dot"></span>
      Nouveau — Prédictions Euro 2026 disponibles
    </div>

    <h1 class="hero-title">
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
      <button class="btn btn-glass" @click="$emit('play-demo')">
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
</template>

<script>
export default {
  name: 'LandingHero',
  data() {
    return {
      isVisible: false
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.isVisible = true
    })
  }
}
</script>
