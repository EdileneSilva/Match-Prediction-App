<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <!-- 2025/2026 Season Selection -->
      <section class="season-highlight gsap-list">
        <div class="season-badge">Ligue 1 - 2025/2026</div>
        <h1>Prédisez le <span class="text-highlight">Futur du Football</span></h1>
        <p class="subtitle">Analyse IA avancée pour la nouvelle saison. Découvrez le tout premier Derby de Paris en Ligue 1.</p>
      </section>

      <!-- Top Affiches / Journée 1 -->
      <section class="matches-section gsap-list">
        <div class="section-header">
          <h2>Journée 1 - Ouverture</h2>
          <span class="date-badge">15 - 17 Août 2025</span>
        </div>
        
        <div class="matches-list">
          <!-- Derby de Paris -->
          <div class="match-item derby-highlight">
            <div class="match-info">
              <span class="derby-tag">LE DERBY DE PARIS</span>
              <div class="match-teams">
                <div class="team">
                  <img src="https://media.api-sports.io/football/teams/85.png" alt="PSG" class="team-logo" />
                  <span>PSG</span>
                </div>
                <span class="vs-text">vs</span>
                <div class="team">
                  <img src="https://media.api-sports.io/football/teams/269.png" alt="Paris FC" class="team-logo" />
                  <span>Paris FC</span>
                </div>
              </div>
            </div>
            <div class="match-meta">
              <div class="match-percentage">82%</div>
              <button class="view-btn magnetic-btn">Analyser</button>
            </div>
          </div>

          <!-- Olympico -->
          <div class="match-item">
            <div class="match-info">
              <div class="match-teams">
                <div class="team">
                  <img src="https://media.api-sports.io/football/teams/81.png" alt="OM" class="team-logo" />
                  <span>OM</span>
                </div>
                <span class="vs-text">vs</span>
                <div class="team">
                  <img src="https://media.api-sports.io/football/teams/80.png" alt="Lyon" class="team-logo" />
                  <span>Lyon</span>
                </div>
              </div>
            </div>
            <div class="match-meta">
              <div class="match-percentage">54%</div>
              <button class="view-btn magnetic-btn">Analyser</button>
            </div>
          </div>

          <!-- Derby du Nord -->
          <div class="match-item">
            <div class="match-info">
              <div class="match-teams">
                <div class="team">
                  <img src="https://media.api-sports.io/football/teams/79.png" alt="Lille" class="team-logo" />
                  <span>Lille</span>
                </div>
                <span class="vs-text">vs</span>
                <div class="team">
                  <img src="https://media.api-sports.io/football/teams/116.png" alt="Lens" class="team-logo" />
                  <span>Lens</span>
                </div>
              </div>
            </div>
            <div class="match-meta">
              <div class="match-percentage">51%</div>
              <button class="view-btn magnetic-btn">Analyser</button>
            </div>
          </div>
        </div>

        <div class="cta-container">
          <router-link to="/predictions" class="cta-btn secondary">Simulation Libre</router-link>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import gsap from 'gsap'

export default {
  name: 'HomeView',
  data() {
    return {
      ctx: null,
      magneticElements: []
    }
  },
  mounted() {
    this.ctx = gsap.context(() => {
      // Entrée de la page principale dynamique
      gsap.fromTo('.main-content',
        { y: -20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }
      );

      // Focus stagger UNIQUEMENT sur les éléments vitaux (Widgets KPIs)
      gsap.fromTo('.gsap-widget',
        { y: 30, opacity: 0, scale: 0.95 },
        { y: 0, opacity: 1, scale: 1, duration: 0.8, stagger: 0.15, ease: "back.out(1.5)", delay: 0.2 }
      );

      // Animation plus douce et sans stagger lourd pour la liste
      gsap.fromTo('.gsap-list',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: "power2.out", delay: 0.5 }
      );

      // Setup simple des boutons magnétiques
      const btns = gsap.utils.toArray('.magnetic-btn');
      btns.forEach(btn => {
        const xTo = gsap.quickTo(btn, "x", {duration: 0.4, ease: "power3", duration: 0.4});
        const yTo = gsap.quickTo(btn, "y", {duration: 0.4, ease: "power3", duration: 0.4});
        
        const mouseMove = (e) => {
          const rect = btn.getBoundingClientRect();
          const x = (e.clientX - (rect.left + rect.width / 2)) * 0.3;
          const y = (e.clientY - (rect.top + rect.height / 2)) * 0.3;
          xTo(x);
          yTo(y);
        };
        
        const mouseLeave = () => {
          xTo(0);
          yTo(0);
        };

        btn.addEventListener('mousemove', mouseMove);
        btn.addEventListener('mouseleave', mouseLeave);

        this.magneticElements.push({ el: btn, move: mouseMove, leave: mouseLeave });
      });

    }, this.$el);
  },
  unmounted() {
    if (this.ctx) {
      this.ctx.revert();
    }
    // Nettoyer les event listeners
    this.magneticElements.forEach(item => {
      item.el.removeEventListener('mousemove', item.move);
      item.el.removeEventListener('mouseleave', item.leave);
    });
  }
}
</script>

<style scoped>
.dashboard {
  padding-bottom: 2rem;
  background-image: linear-gradient(rgba(10, 10, 26, 0.4), rgba(10, 10, 26, 0.6)), url("@/assets/stadium2.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

/* Main Content */
.main-content {
  padding: 100px 2rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Info Cards */
.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.card {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--glass-shadow);
  border: 1px solid var(--glass-border);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.card:hover {
  transform: translateY(-8px);
  border-color: var(--accent-secondary);
  box-shadow: 0 15px 40px rgba(0, 212, 255, 0.2);
}

.card-icon {
  font-size: 2.2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-gradient);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(224, 38, 255, 0.3);
}

.card-content h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-content p {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.score {
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 2rem !important;
  font-weight: 800 !important;
  display: inline-block;
}

/* Matches Section */
.matches-section {
  background: var(--glass-bg);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
}

.matches-section h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(to right, #fff, #a0aec0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.date-badge {
  background: rgba(255, 255, 255, 0.05);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  border: 1px solid var(--glass-border);
}

.season-highlight {
  text-align: center;
  margin-bottom: 4rem;
  margin-top: 2rem;
}

.season-badge {
  display: inline-block;
  background: var(--accent-gradient);
  padding: 0.5rem 1.5rem;
  border-radius: 30px;
  font-weight: 800;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 0 20px rgba(224, 38, 255, 0.4);
}

.season-highlight h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  font-weight: 900;
  letter-spacing: -1px;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.match-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.8rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  transition: all 0.3s ease;
}

.match-item:hover {
  background: var(--glass-hover);
  border-color: var(--accent-secondary);
  transform: scale(1.01) translateX(5px);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
}

.match-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.match-teams {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 1.2rem;
}

.team {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.team-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.1));
}

.match-meta {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.derby-highlight {
  border-left: 4px solid var(--accent-primary);
  background: rgba(224, 38, 255, 0.05);
}

.derby-tag {
  font-size: 0.7rem;
  font-weight: 900;
  color: var(--accent-primary);
  letter-spacing: 2px;
  margin-bottom: 0.2rem;
}

.cta-container {
  margin-top: 2.5rem;
  display: flex;
  justify-content: center;
}

.cta-btn {
  text-decoration: none;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-weight: 700;
  transition: all 0.3s ease;
}

.cta-btn.secondary {
  border: 1px solid var(--accent-secondary);
  color: var(--accent-secondary);
}

.cta-btn.secondary:hover {
  background: rgba(0, 212, 255, 0.1);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}

.view-btn {
  background: var(--accent-gradient);
  color: white;
  border: none;
  padding: 0.7rem 1.8rem;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1;
  position: relative;
  box-shadow: 0 4px 15px rgba(224, 38, 255, 0.3);
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(224, 38, 255, 0.5);
  filter: brightness(1.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 100px 1rem 2rem;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .match-item {
    flex-direction: column;
    gap: 1.2rem;
    text-align: center;
    padding: 1.5rem;
  }

  .match-percentage {
    margin: 0.5rem 0;
  }
  
  .match-teams {
    justify-content: center;
  }
}

</style>
