<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <!-- Info Cards -->
      <section class="info-cards">
        <div class="card gsap-widget">
          <div class="card-icon">📊</div>
          <div class="card-content">
            <h3>Score utilisateur</h3>
            <p class="score">85 pts</p>
          </div>
        </div>
        <div class="card gsap-widget">
          <div class="card-icon">⚽</div>
          <div class="card-content">
            <h3>Matchs</h3>
            <p>12 Matchs prédits</p>
          </div>
        </div>
        <div class="card gsap-widget">
          <div class="card-icon">📈</div>
          <div class="card-content">
            <h3>Statistiques</h3>
            <p>74% Réussite</p>
          </div>
        </div>
      </section>

      <!-- Today's Matches -->
      <section class="matches-section gsap-list">
        <h2>Matchs du jour</h2>
        <div class="matches-list">
          <div class="match-item">
            <div class="match-teams">
              <span>PSG</span>
              <span class="vs-text">vs</span>
              <span>Marseille</span>
            </div>
            <div class="match-percentage">65%</div>
            <button class="view-btn magnetic-btn">Voir</button>
          </div>
          <div class="match-item">
            <div class="match-teams">
              <span>Lyon</span>
              <span class="vs-text">vs</span>
              <span>Lille</span>
            </div>
            <div class="match-percentage">52%</div>
            <button class="view-btn magnetic-btn">Voir</button>
          </div>
          <div class="match-item">
            <div class="match-teams">
              <span>Monaco</span>
              <span class="vs-text">vs</span>
              <span>Nice</span>
            </div>
            <div class="match-percentage">71%</div>
            <button class="view-btn magnetic-btn">Voir</button>
          </div>
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
  min-height: 100vh;
  /* Premium Dark Theme */
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #f8fafc;
  padding-bottom: 2rem;
}

/* Main Content */
.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Info Cards */
.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.card {
  /* Dark Glassmorphism */
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, border-color 0.4s ease;
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 15px 40px rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.card-icon {
  font-size: 2.2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.card-content h3 {
  margin: 0 0 0.5rem 0;
  color: #cbd5e1;
  font-size: 0.95rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-content p {
  margin: 0;
  color: #94a3b8;
  font-size: 1rem;
}

.score {
  color: #f8fafc !important;
  font-size: 1.8rem !important;
  font-weight: 700 !important;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
}

/* Matches Section */
.matches-section {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.matches-section h2 {
  margin: 0 0 1.5rem 0;
  color: #f8fafc;
  font-size: 1.5rem;
  font-weight: 600;
}

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.match-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.match-item:hover {
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
  transform: translateX(5px);
}

.match-teams {
  display: flex;
  gap: 1rem;
  align-items: center;
  font-weight: 500;
  color: #e2e8f0;
  flex: 1;
  font-size: 1.1rem;
}

.match-teams span:first-child,
.match-teams span:last-child {
  font-weight: 600;
}

.vs-text {
  color: #64748b;
  font-size: 0.9rem;
  text-transform: lowercase;
}

.match-percentage {
  font-size: 1.2rem;
  font-weight: bold;
  color: #818cf8;
  margin: 0 2rem;
  text-shadow: 0 0 10px rgba(129, 140, 248, 0.3);
}

.view-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
  z-index: 1;
  position: relative;
}

.view-btn:hover {
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.5);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .match-item {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .match-percentage {
    margin: 0;
  }
}
</style>
